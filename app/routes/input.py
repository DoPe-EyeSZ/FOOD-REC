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
            
            # Atmosphere & Crowds
            "places.goodForGroups",
            "places.goodForChildren",
            
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
            "maxResultCount": 10,
            "includedTypes": ["restaurant"],
            "locationRestriction": {
                "circle": {
                "center": {"latitude": str(lat), "longitude": str(lng)},
                "radius": distance
                }
            },
            "rankPreference": "DISTANCE",
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
            print(json.dumps(response.json(), indent=2))
            return render_template("output.html")
        else:
            print(f"Error {response.status_code}: {response.text}")
            return redirect(request.referrer)
        
        
        

    


