from flask import Blueprint, redirect, url_for, render_template, request, session, flash, jsonify
from data import data_functions, interact_data, cuisine_data
from ML import reccomendation
import pickle


from dotenv import load_dotenv
load_dotenv()



submission = Blueprint("submission", __name__, template_folder="templates")
model = pickle.load(open('ml/models/model.pkl', 'rb'))
scaler = pickle.load(open('ml/models/scaler.pkl', 'rb'))



@submission.route("/", methods = ["POST", "GET"])
def user_submission():
    if request.method == "GET":     #For after user logs in
        return render_template("submission.html")
    
    else:

        #Creating connection
        connection = data_functions.get_connection("test_data_backup.db")
        
        #User's Input
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        max_distance = request.form.get("max_distance")

        top10 = reccomendation.get_recs(lat, lng, max_distance, model, scaler, connection)

        if top10 is None:
            connection.close()
            return "Error"
        
        session["suggestions"] = top10
        print(len(session["suggestions"]))
        session["index"] = 0
        print(session["index"])
            
        connection.close()    
        return redirect(url_for("submission.show_restaurant"))
    

@submission.route("/show_restaurant")
def show_restaurant():
    suggestions = session["suggestions"]
    index = session["index"]

    print(f"{index+1} restaurant")
    restaurant_to_display = suggestions[index]
    

    return render_template("display_restaurant.html", displayed_restaurant = restaurant_to_display)


@submission.route("/process_response", methods = ["POST"])
def process_response():
    connection = data_functions.get_connection("test_data_backup.db")
    session["index"] += 1
    
    response = request.form.get("response")
    place_id = request.form.get("place_id")
    cuisine = request.form.get("cuisine")
    rating = request.form.get("rating")
    rating_count = request.form.get("rating_count")
    opening = request.form.get("is_open")
    drive_time = request.form.get("drive_time")

    #Saving interaction
    interact_data.insert_interaction(connection, place_id, rating, rating_count, opening, drive_time, response, user_id="test_user")

    #Increment acceptance
    if response == "1":
        print("accepted")
        cuisine_data.increment_acceptance(connection, cuisine, user_id="test_user")


    if session["index"] < len(session["suggestions"]):
        connection.close()
        return redirect(url_for("submission.show_restaurant"))
    
    else:
        reccent_10 = data_functions.join_10_restaurant(connection, user_id="test_user")
        connection.close()
        print(reccent_10)
        return render_template("summary.html")

        
        
        
        
    


