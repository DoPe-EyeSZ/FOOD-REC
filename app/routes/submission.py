from flask import Blueprint, redirect, url_for, render_template, request, session, flash, jsonify
from sklearn.model_selection import train_test_split
import json
from api import api_function
from data import cuisine_data, data_functions, interact_data, restaurant_data, user_data

from dotenv import load_dotenv
load_dotenv()



submission = Blueprint("submission", __name__, template_folder="templates")




@submission.route("/", methods = ["POST", "GET"])
def user_submission():
    if request.method == "GET":     #For after user logs in
        return render_template("submission.html")
    
    else:

        connection = data_functions.get_connection("test_data.db")
        
        cuisine_data.create_cuisine_table(connection)
        restaurant_data.create_restaurant_table(connection)
        interact_data.create_interact_table(connection)
        user_data.create_user_table(connection)

        #User's Input
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        max_distance = request.form.get("max_distance")

        response = api_function.use_api(lat, lng, max_distance)

        if response.status_code == 200:
            data = response.json()

            feature_data = api_function.extract_api_data(data)

            #List which contains lists of feature data (NAME and ID not included)
            clean_feature_data = []        
            for place_dict in feature_data:
                    dine_in = place_dict["dineIn"]
                    takeout = place_dict["takeout"]
                    vegan = place_dict["vegan"]
                    price = place_dict["price_level"]
                    cuisine = place_dict["cuisine"]
                    rating = place_dict["rating"]
                    rating_count = place_dict["rating_count"]
                    opening = place_dict["is_open"]
                    drive = place_dict["drive_time"]

                    restaurnt = [dine_in, takeout, vegan, price, cuisine, rating, rating_count, opening, drive, -1]
                    
                    print("upsert db here")
                    print("add cuisine shown but not accept here")
                    clean_feature_data.append(restaurnt)


            #Return dictionary of cuisine frequency
            frequency_dict = api_function.find_frequency(connection)        


            #Retrieve feature data with cuisine frequency inserted
            updated_features, no_use = api_function.insert_frequency(clean_feature_data, frequency_dict)
            
            
            return render_template("output.html")
        

        else:

            print(f"Error {response.status_code}: {response.text}")
            return redirect(request.referrer)
        
        
        
    


