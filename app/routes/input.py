from flask import Blueprint, redirect, url_for, render_template, request, session, flash, jsonify
import requests
import json
import os


input = Blueprint("input", __name__, template_folder="templates")

GOOGLE_API_KEY = os.environ.get("google_api_key")


@input.route("/", methods = ["POST", "GET"])
def user_input():
    if request.method == "GET":     #For after user logs in
        return render_template("input.html")
    
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
            print(extract_api_data(data))
            return render_template("output.html")
        else:
            print(f"Error {response.status_code}: {response.text}")
            return redirect(request.referrer)
        
        
#Extract important data so it can be easily accessable
def extract_api_data(data):
    if "places" in data:
        information = []
        for place in data["places"]:

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
            
            resturant = [id, rating, rating_count, takeout, dineIn, vegan, open]
            information.append(resturant)

        for index, value in enumerate(data["routingSummaries"]):
            drive_time = value["legs"][0]["duration"]
            drive_time = drive_time[:len(drive_time)-1]
            information[index].append(int(drive_time))

    return information      #[avg rating, num ratings, takeout, dinein, vegan option, open, drive time]

            
            
            
            
            
            
    


