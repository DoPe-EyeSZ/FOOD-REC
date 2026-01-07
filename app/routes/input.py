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
        url = 'https://places.googleapis.com/v1/places:searchNearby'

        lat = request.form.get('lat')
        lng = request.form.get('lng')
        max_price = request.form.get("max_price")
        max_distance = request.form.get("max_distance")

        distance = round((1609.34 * int(max_distance)), 2)

        print(f"latitude {lat} | longditiude {lng} | distance {distance} | max price {max_price}")
        

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": GOOGLE_API_KEY,
            "X-Goog-FieldMask": "places.currentOpeningHours.openNow,places.priceLevel,places.displayName,places.formattedAddress,places.id"
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
            "rankPreference": "DISTANCE"

        }

        response = requests.post(url, headers= headers, json=params)

        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error {response.status_code}: {response.text}")
        
        return render_template("output.html")
        

    


