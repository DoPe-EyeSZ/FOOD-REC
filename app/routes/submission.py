from flask import Blueprint, redirect, url_for, render_template, request, session, flash, jsonify
import requests
import json
import os


submission = Blueprint("submission", __name__, template_folder="templates")

GOOGLE_API_KEY = os.environ.get("google_api_key")

cuisine_stats = {}

@submission.route("/", methods = ["POST", "GET"])
def user_submission():
    if request.method == "GET":     #For after user logs in
        print()
        return render_template("submission.html")
    
    else:
        url = 'https://places.googleapis.com/v1/places:searchNearby'        #Url for Google Places

        #User's request/data
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        max_price = request.form.get("max_price")
        max_distance = request.form.get("max_distance")

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
            "maxResultCount": 20,
            "includedPrimaryTypes": ["restaurant"],
            "locationRestriction": {
                "circle": {
                "center": {"latitude": str(lat), "longitude": str(lng)},
                "radius": distance
                }
            },
            "rankPreference": "POPULARITY",
            "routingParameters": {
                "origin": {
                    "latitude": float(lat),
                    "longitude": float(lng)
                },
                "travelMode": "DRIVE"
            } 

        }

        response = requests.post(url, headers= headers, json=params)

        if response.status_code == 200:

            
            data = response.json()
            #print(json.dumps(response.json(), indent=2))
            print(extract_api_data(data, cuisine_stats))
            print(cuisine_stats)
            return render_template("output.html")
        

        else:

            print(f"Error {response.status_code}: {response.text}")
            return redirect(request.referrer)
        
        
#Extract important data so it can be easily accessable
def extract_api_data(data, cuisine_stats):
    if "places" in data:
        information = []
        for place in data["places"]:

            #TEST PURPOSES---------------------
            print(place)
            answer = input("yes or no to resturant?")

            ans = None

            if answer == "yes":
                ans = 1
            else:
                ans = 0

            #-----------------------------
            id = place["id"]

            rating = place["rating"]

            rating_count = place["userRatingCount"]

            takeout = 0
            if "takeout" in place:
                if place["takeout"]:
                    takeout = 1

            dineIn = 0
            if "dineIn" in place:
                if place["dineIn"]:
                    dineIn = 1

            vegan = 0
            if "servesVegetarianFood" in place:
                if place["servesVegetarianFood"]:
                    vegan = 1

            open = 0
            if "openNow" in place["currentOpeningHours"]:
                if place["currentOpeningHours"]["openNow"]:
                    open = 1
            
            resturant = [ans, id, rating, rating_count, takeout, dineIn, vegan, open]
            information.append(resturant)

            #Updates cuisine stats (accepted/shown)
            if "primaryType" in place:
                cuisine = place["primaryType"]
                if cuisine in cuisine_stats:
                    cuisine_stats[cuisine]["shown"] += 1
                else:
                    cuisine_stats[cuisine] = {"shown": 1, "accepted": 0}

        for index, value in enumerate(data["routingSummaries"]):
            drive_time = value["legs"][0]["duration"]
            drive_time = drive_time[:len(drive_time)-1]
            information[index].append(int(drive_time))

    return information      #[avg rating, num ratings, takeout, dinein, vegan option, open, drive time]

            
            
            
            
            
            
    


