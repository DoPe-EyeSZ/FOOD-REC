#Flask tools
from flask import Blueprint, redirect, url_for, render_template, request, session, flash, jsonify

#Security
from werkzeug.security import generate_password_hash, check_password_hash

#Data functions
from data import data_functions, interact_data, cuisine_data, user_data, restaurant_data

#ML functions
from ML import reccomendation
import pickle

from app import limiter

#Loading api keys
from dotenv import load_dotenv
load_dotenv()


submission = Blueprint("submission", __name__, template_folder="templates")

#Updated model/scaler
model = pickle.load(open('ml/models/model.pkl', 'rb'))
scaler = pickle.load(open('ml/models/scaler.pkl', 'rb'))


@submission.route("/", methods = ["POST", "GET"])
@submission.route("/login", methods = ["POST", "GET"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        connection = data_functions.get_connection("prod")
        user_name = request.form.get("username")
        password = request.form.get("password")

        user_credentials = user_data.fetch_user_credentials(connection, user_name)
        

        if user_credentials and check_password_hash(user_credentials[1], password):
            session["user_id"] = user_credentials[0]
            connection.close()
            flash("succesffuly logged in")
            return redirect(url_for("submission.user_submission"))
            
        else:
            flash("Wrong username or password", "warning")
            return redirect(url_for("submission.login"))
            

    else:

        return render_template("login.html")


@submission.route("/logout", methods = ["GET"])
@limiter.limit("5 per minute")
def logout():
    if "user_id" in session:
        session.clear()
        flash("Successfully logged out!", "success")
    
    else:
        flash("You're not logged in", "warning")

    return redirect(url_for("submission.login"))



@submission.route("/signup", methods = ["POST", "GET"])
@limiter.limit("10 per minute")
def signup():

    if "user_id" in session:
        flash("ur already logged in")
        return redirect(url_for("submission.user_submission"))

    else:
        #After user submits signup form
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            password_check = request.form.get("password_check")
            connection = data_functions.get_connection("prod")

            #Create new account if user does not exist
            if not user_data.fetch_user_credentials(connection, username):

                #If user reenters password correctly
                if password == password_check:
                    pw_hash = generate_password_hash(password)
                    user_data.create_user(connection, username, pw_hash)
                    user_id = user_data.fetch_user_credentials(connection, username)[0]
                    session["user_id"] = user_id
                    flash("user created")
                    return redirect(url_for("submission.user_submission"))
                
                else:
                    flash("You password does not match", "warning")

            #User name already exists
            else:
                flash("Username already exists", "warning")

        return render_template("signup.html")


@submission.route("/user_submission", methods = ["POST", "GET"])
@limiter.limit("10 per hour")
def user_submission():
    if "user_id" in session:
        if request.method == "GET":     #For after user logs in
            connection = data_functions.get_connection("prod")
            return render_template("submission.html")

        else:

            #Creating connection
            connection = data_functions.get_connection("prod")
            
            #User's Input
            lat = request.form.get('lat')
            lng = request.form.get('lng')
            max_distance = request.form.get("max_distance")

            top10 = reccomendation.get_recs(lat, lng, max_distance, model, scaler, connection, user_id = session["user_id"])

            if top10 is None:
                connection.close()
                return render_template("error_page.html")
            
            session["suggestions"] = top10
            session["index"] = 0
                
            connection.close()    
            return redirect(url_for("submission.show_restaurant"))
    
    else:
        return redirect(url_for("submission.login"))
    

@submission.route("/show_restaurant")
def show_restaurant():
    if "user_id" in session:
        suggestions = session["suggestions"]
        index = session["index"]

        restaurant_to_display = suggestions[index]
        restaurant_to_display[0]["cuisine"] = restaurant_to_display[0]["cuisine"].replace("_", " ").title()
        
        return render_template("display_restaurant.html", displayed_restaurant = restaurant_to_display)
    
    else:
        return redirect(url_for("submission.login"))


@submission.route("/process_response", methods = ["POST"])
def process_response():
    if "user_id" in session:
        connection = data_functions.get_connection("prod")
        session["index"] += 1
        
        response = request.form.get("response")
        place_id = request.form.get("place_id")
        cuisine = request.form.get("cuisine")
        cuisine = cuisine.replace(" ", "_").lower()
        rating = request.form.get("rating")
        rating_count = request.form.get("rating_count")
        opening = request.form.get("is_open")
        drive_time = request.form.get("drive_time")
        dine_in = request.form.get("dineIn")
        name = request.form.get("name")
        price_level = request.form.get("price_level")
        takeout = request.form.get("takeout")
        vegan = request.form.get("vegan")

        #Saving interaction
        interact_data.insert_user_interaction(connection, place_id, rating, rating_count, opening, drive_time, response, user_id=session["user_id"])
        
        #Saving Restaurant data
        restaurant_data.insert_restaurant(connection, place_id, dine_in, takeout, vegan, price_level, cuisine, name)

        #Saving cuisine
        cuisine_data.upsert_cuisine_stats(connection, cuisine, int(response), session["user_id"])

        #Increment acceptance
        if response == "1":
            cuisine_data.increment_acceptance(connection, cuisine, user_id = session["user_id"])

        #Continue to show suggested restaurants
        if session["index"] < len(session["suggestions"]):
            connection.close()
            return redirect(url_for("submission.show_restaurant"))
        
        #All restaurants has been shown
        else:
            #ORDER: name, dinein, takeout, vegan, price, cuisine, rating, rating count, opening, drive, acceptance
            reccent_10_tuple = data_functions.join_10_restaurant(connection, user_id = session["user_id"])[::-1]
            suggestions = session["suggestions"]

            #Stores all data for front end
            full_summary = []

            
            
            price_map = {
                    5: "$",
                    4: "$$", 
                    3: "$$$",
                    2: "$$$$",
                    1: "$$$$$"
                }
            
            #Combines important feature data with acceptance probability
            for x in range(10):
                restaurant = list(reccent_10_tuple[x])      #Retrieve individual restaurant 
  
                probability = suggestions[x][1]*100
                restaurant.append(round(probability, 2))        #Convert probability to percentage

                restaurant[4] = price_map.get(restaurant[4], "N/A")     #Replace pricing number w '$'

                restaurant[5] = restaurant[5].replace("_", " ").title()     #Formalize cuisine display

                full_summary.append(restaurant)
                
            keys = ["name", "dine_in", "take_out", "vegan", "price", "cuisine", 
                "rating", "rating_count", "open", "drive", "accept", "accept_prob"]

            #Convert to dictionary
            suggested_restaurant = [dict(zip(keys, place)) for place in full_summary]
                

            connection.close()
            return render_template("summary.html", displayed_restaurants = suggested_restaurant)
        
    else:
        return redirect(url_for("submission.login"))


@submission.route("/statistics", methods = ["GET"])
@limiter.limit("10 per minute")
def statistics():
    if "user_id" in session:
        connection = data_functions.get_connection("prod")
        frontend_data = {}

        all_cuisines = cuisine_data.fetch_all_cuisine(connection, session["user_id"])
        all_interactions = interact_data.fetch_user_interactions(connection, session["user_id"])

        highest_appearance = []
        highest_acceptance = []

        for info in all_cuisines:
            cuisine = info[1].replace("_", " ").title()
            appear = info[2]
            accept = info[3]

            ratio = round((accept/appear)*100, 2)            
            if appear > 3 and ratio > 50:
                highest_acceptance.append([cuisine, ratio])
            highest_appearance.append([cuisine, appear])

        highest_appearance.sort(key = lambda c: c[1], reverse=True)
        highest_acceptance.sort(key = lambda c:c[1], reverse=True)

        frontend_data["highest_appearance"] = highest_appearance[:10]       #Cuisine user seen the most
        frontend_data["highest_acceptance"] = highest_acceptance[:10]       #Cuisine user likes the most (with ratio)
        frontend_data["all_cuisine_len"] = len(all_cuisines)        #Number of cuisines users have seen
        frontend_data["all_interaction_len"] = len(all_interactions)        #Number of restaurants interacted with

        

        '''
        Cuisine not specified for cusind named "restuarnt"
        show what we think they care about the most for restaurant
        '''
        
        return render_template("stats.html", frontend_data = frontend_data)

    else:
        return redirect(url_for("submission.login"))
    

@submission.route("/delete_user", methods = ["GET"])
def delete_user():
    if "user_id" in session:
        x = input("y for delete; n for no")
        if x == "y":
            user_id = session["user_id"]
            connection = data_functions.get_connection("prod")
            interact_data.delete_user_interactions(connection, user_id)
            cuisine_data.delete_cuisines(connection, user_id)
            user_data.delete_user(connection, user_id)

        session.clear()

    return redirect(url_for("submission.login"))
        
        
        
    


