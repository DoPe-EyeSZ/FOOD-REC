from flask import Blueprint, redirect, url_for, render_template, request, session, flash, jsonify
from sklearn.model_selection import train_test_split
import requests
import json
import time
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

        # SoCal locations with food options (lat, lng, location_name)
        locations = [
            # Your 3 specified locations
            (34.0381, -117.8648, "The Village at Walnut"),
            (33.9533, -117.7320, "The Shoppes at Chino Hills"),
            (33.6846, -117.8265, "Irvine Spectrum Center"),
            
            # Additional SoCal locations with many food options
            (34.0689, -118.4452, "Century City Westfield"),
            (33.7701, -118.1937, "Long Beach Downtown"),
            (34.1478, -118.1445, "Pasadena Old Town"),
            (33.5427, -117.7854, "The Crossroads at Mission Viejo"),
            (33.8366, -117.9143, "The Outlets at Orange"),
            (34.1808, -118.3090, "Universal CityWalk"),
            (33.5950, -117.8620, "Laguna Hills Mall Area"),
            (34.0195, -118.4912, "Santa Monica Third Street Promenade"),
            (33.8303, -118.3416, "Del Amo Fashion Center"),
            (34.1416, -117.9227, "Monrovia Downtown"),
            (33.7175, -117.9542, "The District at Tustin Legacy"),
            (34.0407, -117.5098, "Victoria Gardens, Rancho Cucamonga")
        ]

        # Initialize data storage
        all_feature_data = []
        result = []

        # Run 15 API calls
        for i in range(15):
            location = locations[i]
            lat = location[0]
            lng = location[1]
            location_name = location[2]
            max_distance = 8  # 8 miles
            
            print(f"\n{'='*60}")
            print(f"Loop {i+1}/15: {location_name}")
            print(f"Coordinates: ({lat}, {lng})")
            print(f"Max Distance: {max_distance} miles")
            print(f"{'='*60}")
            
            # Make API call
            response = use_api(lat, lng, None, max_distance)  # max_price not used
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract data
                info = extract_api_data(data, cuisine_stats)
                feature_data = info[0]  # List of restaurant features
                results = info[1]       # List of binary results
                
                # Append to centralized lists
                all_feature_data.extend(feature_data)
                result.extend(results)
                
                print(f"Retrieved {len(feature_data)} restaurants")
                print(f"Feature data sample: {feature_data[:2]}")  # Show first 2
                
            else:
                print(f"ERROR {response.status_code}: {response.text}")
            
            # Delay between API calls (except for last iteration)
            if i < 14:
                time.sleep(1)

        print(f"\n{'='*60}")
        print(f"DATA COLLECTION COMPLETE")
        print(f"{'='*60}")
        print(f"Total restaurants collected: {len(all_feature_data)}")
        print(f"Total results: {len(result)}")
        print(f"Cuisine stats: {cuisine_stats}")

        # Now process the data
        print(f"\n{'='*60}")
        print("PROCESSING DATA")
        print(f"{'='*60}")

        # Remove IDs from feature data
        clean_feature_data = remove_id(all_feature_data)
        print(f"IDs removed. Clean feature data length: {len(clean_feature_data)}")

        # Calculate acceptance/rejection frequencies
        frequencies = find_frequency(cuisine_stats)
        print(f"Frequencies calculated: {frequencies}")

        # Insert frequencies into feature data (replaces cuisine string with ratio)
        new_data = insert_frequency(clean_feature_data, frequencies)
        print(f"Frequencies inserted. New data length: {len(new_data)}")
        print(f"Sample of processed data: {new_data[:3]}")

        # Train model
        print(f"\n{'='*60}")
        print("TRAINING MODEL")
        print(f"{'='*60}")

        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression

        x_train, x_test, y_train, y_test = train_test_split(new_data, result, test_size=0.2, random_state=42)

        print(f"Training set size: {len(x_train)}")
        print(f"Test set size: {len(x_test)}")

        clf = LinearRegression()
        clf.fit(x_train, y_train)

        predictions = clf.predict(x_test)
        print(f"\nPredictions (first 10): {predictions[:10]}")
        print(f"Actual values (first 10): {y_test[:10]}")
        print(f"Accuracy: {clf.score(x_test, y_test)}")

        print(f"\n{'='*60}")
        print("TEST COMPLETE")
        print(f"{'='*60}")
        return render_template("output.html")
        
        
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
                resturant.append(cuisine)
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

            

def remove_id(data):        #Removes resturant ID from feature data to feed to ML
    for i in range(len(data)):
        data[i] = data[i][1:]
    return data

def find_frequency(data):       #Find how often user accept/skips food
    for cuisine, frequency in data.items():
        accepted = frequency["accepted"]
        shown = frequency["shown"]
        frequency = round(float(accepted/shown), 2)
        data[cuisine] = frequency
    return data

def insert_frequency(data, freq):       #Insert frequency into cleaned data
    for place in data:
        cuisine = place[-1]
        place[-1] = freq[cuisine]

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
        "maxResultCount": 20,
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
    


