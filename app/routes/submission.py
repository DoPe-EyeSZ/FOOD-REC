from flask import Blueprint, redirect, url_for, render_template, request, session, flash, jsonify
from sklearn.model_selection import train_test_split
import requests
import json
import os


submission = Blueprint("submission", __name__, template_folder="templates")

GOOGLE_API_KEY = os.environ.get("google_api_key")

cuisine_stats = {}
price_levels = {
    "PRICE_LEVEL_FREE": 5,
    "PRICE_LEVEL_INEXPENSIVE": 4,
    "PRICE_LEVEL_MODERATE": 3,
    "PRICE_LEVEL_EXPENSIVE": 2,
    "PRICE_LEVEL_VERY_EXPENSIVE": 1
}

@submission.route("/", methods = ["POST", "GET"])
def user_submission():
    if request.method == "GET":     #For after user logs in
        return render_template("submission.html")
    
    else:

        #User's request/data
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        max_price = request.form.get("max_price")
        max_distance = request.form.get("max_distance")

        response = use_api(lat, lng, max_price, max_distance)

        if response.status_code == 200:

            
            data = response.json()
            #print(json.dumps(response.json(), indent=2))
            info = extract_api_data(data, cuisine_stats)
            all_feature_data = info[0]
            result = info[1]
            clean_feature_data = remove_id(all_feature_data)

            '''x_train, x_test, y_train, y_test = train_test_split(clean_feature_data, result, test_size=0.2)
            from sklearn.linear_model import LinearRegression
            clf = LinearRegression()
            clf.fit(x_train, y_train)
            print(clf.predict(x_test))
            print(y_test)
            print(f"Accuracy: {clf.score(x_test, y_test)}")'''#ML Part
            
            return render_template("output.html")
        

        else:

            print(f"Error {response.status_code}: {response.text}")
            return redirect(request.referrer)
        
        
#Extract important data so it can be easily accessable
def extract_api_data(data, cuisine_stats):
    if "places" in data:
        information = [[],[]]
        for place in data["places"]:

            print(place)
            print("===============================================")
            if "generativeSummary" in place:
                print(f"Summary: {place["generativeSummary"]["overview"]["text"]}")

            id = place["id"]

            if "rating" in place:
                rating = place["rating"]
                rating_count = place["userRatingCount"]
                print(f"Rating: {rating}")
                print(f"Rating Count: {rating_count}")

            if "priceLevel" in place:
                price_level = price_levels.get(place["priceLevel"], 0)
            else:
                price_level = 0

            print(f"price level: {price_level}")

            takeout = 0
            if "takeout" in place:
                if place["takeout"]:
                    takeout = 1
                    print(f"Allows Takeout")

            dineIn = 0
            if "dineIn" in place:
                if place["dineIn"]:
                    dineIn = 1
                    print(f"Allows Dine in")

            vegan = 0
            if "servesVegetarianFood" in place:
                if place["servesVegetarianFood"]:
                    vegan = 1
                    print(f"Has Vegitarian Options")

            open = 0
            if "currentOpeningHours" in place:
                if "openNow" in place["currentOpeningHours"]:
                    if place["currentOpeningHours"]["openNow"]:
                        open = 1
                        print(f"Currently Open")

            #TEST PURPOSES---------------------
            print(f"Name: {place["displayName"]["text"]}")
            answer = input("yes or no to resturant?\n")

            accept = False

            if answer == "y":
                accept = True

            #-----------------------------
            
            resturant = [id, rating, rating_count, price_level, takeout, dineIn, vegan, open]
            print("----------------------------------------")   #TEST


            #Updates cuisine stats (accepted/shown)
            if "primaryType" in place:
                cuisine = place["primaryType"]
                if cuisine in cuisine_stats:
                    cuisine_stats[cuisine]["shown"] = cuisine_stats[cuisine].get("shown", 0) + 1
                else:
                    cuisine_stats[cuisine] = {"shown": 1, "accepted": 0}

                if accept:
                    cuisine_stats[cuisine]["accepted"] = cuisine_stats[cuisine].get("accepted", 0) + 1
                    information[1].append(1)
                else:
                    information[1].append(0)

            print(resturant)
            information[0].append(resturant)
        
        #appends drive time to restaurant info
        for index, value in enumerate(data["routingSummaries"]):
            drive_time = value["legs"][0]["duration"]
            drive_time = drive_time[:len(drive_time)-1]
            information[0][index].insert(len(information[0][index])-1,int(drive_time))

    return information      #[[id, rating, num ratings, price level, takeout, dinein, vegan option, open, drive time], [accept/rejection]]

            

def remove_id(data):
    for i in range(len(data)):
        data[i] = data[i][1:]
    return data



def use_api(lat, lng, max_price, max_distance):

    url = 'https://places.googleapis.com/v1/places:searchNearby'        #Url for Google Places

    distance = round((1609.34 * int(max_distance)), 2)      #Convert from miles to meters
        
    #Returned data from API request
    fields = [
        # Rep and cost
        "places.rating",
        "places.userRatingCount",
        "places.priceLevel",
        
        # Environment
        "places.primaryType",           # Cuisine
        "places.generativeSummary.overview",     # AI summary of review
        
        # Service options
        "places.dineIn",
        "places.takeout",
        "places.servesVegetarianFood",  # Vegan
        
        # Distance (Requires routingParameters in the body)
        "routingSummaries",      # Drive Distance

        #Basic Meta Data
        "places.formattedAddress",
        "places.displayName.text",
        "places.id",
        "places.currentOpeningHours.openNow"
    ]


    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": ",".join(fields)
    }

    params = {
        "maxResultCount": 5,
        "includedPrimaryTypes": ["restaurant"],
        "locationRestriction": {
            "circle": {
            "center": {"latitude": str(lat), "longitude": str(lng)},
            "radius": distance
            }
        },
        "routingParameters": {
            "origin": {
                "latitude": float(lat),
                "longitude": float(lng)
            },
            "travelMode": "DRIVE"
        },
        "minRating": 0.0,

        "priceLevels": [
            "PRICE_LEVEL_FREE",
            "PRICE_LEVEL_INEXPENSIVE",
            "PRICE_LEVEL_MODERATE",
            "PRICE_LEVEL_EXPENSIVE",
            "PRICE_LEVEL_VERY_EXPENSIVE"
        ] 

    }

    return requests.post(url, headers= headers, json=params)
    


