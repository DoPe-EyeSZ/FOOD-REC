#Flask tools
from flask import Blueprint, redirect, url_for, render_template, request, session, flash, jsonify

#Security
from werkzeug.security import generate_password_hash, check_password_hash

#Data functions
from data import data_functions, interact_data, cuisine_data, user_data, restaurant_data, user_model_data

#ML functions
from ML import reccomendation, ml_model
import pickle

from app import limiter

#Loading api keys
from dotenv import load_dotenv
load_dotenv()


submission = Blueprint("submission", __name__, template_folder="templates")


@submission.route("/", methods = ["POST", "GET"])
@submission.route("/login", methods = ["POST", "GET"])
@limiter.limit("10 per minute")
def login():
    if request.method == "POST":
        connection = data_functions.get_connection("prod")
        try:
            #Creating table
            user_data.create_user_table(connection)
            restaurant_data.create_restaurant_table(connection)
            connection.commit()

            user_name = request.form.get("username")
            password = request.form.get("password")

            user_credentials = user_data.fetch_user_credentials(connection, user_name)
            

            if user_credentials and check_password_hash(user_credentials[1], password):
                session["user_id"] = user_credentials[0]
                flash("Login Successful")
                return redirect(url_for("submission.user_submission"))
                
            else:
                flash("Wrong username or password", "warning")
                return redirect(url_for("submission.login"))
            
        except Exception as e:
            print(f"Error: {e}")
            return render_template("error_page.html")
        
        finally:
            if 'connection' in locals():
                    connection.close()

    else:

        return render_template("login.html")


@submission.route("/logout", methods = ["GET"])
@limiter.limit("5 per minute")
def logout():
    if "user_id" in session:
        session.clear()
        flash("Logout Successful", "success")
    
    else:
        flash("You're not logged in", "warning")

    return redirect(url_for("submission.login"))



@submission.route("/signup", methods = ["POST", "GET"])
@limiter.limit("10 per minute")
def signup():

    if "user_id" in session:
        flash("You're already logged in")
        return redirect(url_for("submission.user_submission"))

    else:
        connection = data_functions.get_connection("prod")
        try:
            #After user submits signup form
            if request.method == "POST":

                username = request.form.get("username")
                password = request.form.get("password")
                password_check = request.form.get("password_check")

                user_data.create_user_table(connection)
                restaurant_data.create_restaurant_table(connection)
                connection.commit()

                #Create new account if user does not exist
                if not user_data.fetch_user_credentials(connection, username):

                    #If user reenters password correctly
                    if password == password_check:
                        pw_hash = generate_password_hash(password)
                        user_data.create_user(connection, username, pw_hash)
                        user_id = user_data.fetch_user_credentials(connection, username)[0]
                        session["user_id"] = user_id
                        flash("Account successfully created")
                        return redirect(url_for("submission.user_submission"))
                    
                    else:
                        flash("Your password does not match", "warning")

                #User name already exists
                else:
                    flash("Username already exists", "warning")
                

            return render_template("signup.html")
        
        except Exception as e:
            print(f"Error: {e}")

        finally:
            if connection:
                connection.close()




@submission.route("/user_submission", methods = ["POST", "GET"])
@limiter.limit("5 per hour")
def user_submission():
    if "user_id" not in session:
        return redirect(url_for("submission.login"))

    connection = data_functions.get_connection("prod")
    try:
        
        user_model_data.create_user_models_table(connection)
        interact_data.create_interact_table(connection)
        cuisine_data.create_cuisine_table(connection)
        connection.commit()

        #For after user logs in
        if request.method == "GET":     
            curr_interactions = interact_data.fetch_user_interactions(connection, session["user_id"])
            
            #Cold start with NO interactions
            if len(curr_interactions) < 10:     
                flash("Let’s train on a bit of data so we can learn your preferences.")
                
                suggestions = reccomendation.get_recs(34.0961, -118.1058, 5, None, None, connection, session["user_id"], True)
                suggestions += reccomendation.get_recs(40.6815, -73.8365, 5, None, None, connection, session["user_id"], True)
                suggestions += reccomendation.get_recs(37.3394, -121.8950, 5, None, None, connection, session["user_id"], True)


                session["suggestions"] = suggestions
                session["index"] = 0
                session["training"] = True

                return redirect(url_for("submission.show_restaurant"))


            #Retrain after 50 data sets
            old_interaction_count = user_model_data.fetch_model_data(connection, session["user_id"])[4]
            if (len(curr_interactions) - old_interaction_count) >= 50:       #50 or more new interactions
                ml_model.train_save_model(connection, session.get("user_id"), coldstart=False, prod_mode=True)        


            return render_template("submission.html")

        else:
        
            #User's Input
            lat = request.form.get('lat')
            lng = request.form.get('lng')
            max_distance = request.form.get("max_distance")

            #Load model
            model, scaler = user_model_data.load_user_model(connection, session["user_id"])

            top10 = reccomendation.get_recs(lat, lng, max_distance, model, scaler, connection, user_id = session["user_id"], training= False)

            if top10 is None:
                return render_template("error_page.html")
            
            session["suggestions"] = top10
            session["index"] = 0
                
            return redirect(url_for("submission.show_restaurant"))
        

    except Exception as e:
        print(f"Error: {e}")
        return render_template("error_page.html")

    finally:
        if 'connection' in locals():
            connection.close()
            
    
    

@submission.route("/show_restaurant")
@limiter.limit("30 per minute")
def show_restaurant():
    if "user_id" in session:
        suggestions = session["suggestions"]
        index = session["index"]

        price_map = {
                    5: "$",
                    4: "$$", 
                    3: "$$$",
                    2: "$$$$",
                    1: "$$$$$"
                }
        
        try:
            if "training" in session:
                restaurant_to_display = suggestions[index]
                restaurant_to_display["cuisine"] = restaurant_to_display["cuisine"].replace("_", " ").title()
                restaurant_to_display["price_level"] = price_map.get(restaurant_to_display["price_level"], "N/A")
            else:
                restaurant_to_display = suggestions[index][0]
                restaurant_to_display["cuisine"] = restaurant_to_display["cuisine"].replace("_", " ").title()
                restaurant_to_display["price_level"] = price_map.get(restaurant_to_display["price_level"], "N/A")
            
            return render_template("display_restaurant.html", displayed_restaurant = restaurant_to_display, training = session.get("training", False))
        
        except Exception as e:
            print(f"Error: {e}")
            return render_template("error_page.html")
        
    else:
        return redirect(url_for("submission.login"))


@submission.route("/process_response", methods = ["POST"])
@limiter.limit("30 per minute")
def process_response():
    if "user_id" in session:

        price_to_num = {"$": 5, "$$": 4, "$$$": 3, "$$$$": 2, "$$$$$": 1}
        num_to_price = {5: "$",4: "$$", 3: "$$$", 2: "$$$$", 1: "$$$$$"}
        
        
        connection = data_functions.get_connection("prod")
        session["index"] = session.get("index", 0) + 1
        
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
        price_level = price_to_num.get(str(price_level), 0)
        takeout = request.form.get("takeout")
        vegan = request.form.get("vegan")

        try:
            #Saving Restaurant data
            restaurant_data.insert_restaurant(connection, place_id, dine_in, takeout, vegan, price_level, cuisine, name)
            
            #Saving interaction
            interact_data.insert_user_interaction(connection, place_id, rating, rating_count, opening, drive_time, response, user_id=session["user_id"])

            #Saving cuisine
            cuisine_data.upsert_cuisine_stats(connection, cuisine, int(response), session["user_id"])
        


            #Continue to show suggested restaurants
            if session["index"] < len(session["suggestions"]):
                return redirect(url_for("submission.show_restaurant"))
            
            #All restaurants has been shown
            else:
                if "training" in session:
                    flash("Training is done. Our accuracy will improve as you continue")

                    ml_model.train_save_model(connection, session["user_id"], coldstart=True, prod_mode=True)
                    session.pop("training", None)
                    return redirect(url_for("submission.user_submission"))
                
                #ORDER: name, dinein, takeout, vegan, price, cuisine, rating, rating count, opening, drive, acceptance
                reccent_10_tuple = data_functions.join_10_restaurant(connection, user_id = session["user_id"])[::-1]
                suggestions = session["suggestions"]

                #Stores all data for front end
                full_summary = []

                
                #Combines important feature data with acceptance probability
                for x in range(10):
                    restaurant = list(reccent_10_tuple[x])      #Retrieve individual restaurant 
    
                    probability = suggestions[x][1]*100
                    restaurant.append(round(probability, 2))        #Convert probability to percentage

                    restaurant[4] = num_to_price.get(restaurant[4], "N/A")     #Replace pricing number w '$'

                    restaurant[5] = restaurant[5].replace("_", " ").title()     #Formalize cuisine display

                    full_summary.append(restaurant)
                    
                keys = ["name", "dine_in", "take_out", "vegan", "price", "cuisine", 
                    "rating", "rating_count", "open", "drive", "accept", "accept_prob"]

                #Convert to dictionary
                suggested_restaurant = [dict(zip(keys, place)) for place in full_summary]
                    

                return render_template("summary.html", displayed_restaurants = suggested_restaurant)
            
        except Exception as e:
            print(f"Error: {e}")
            return render_template("error_page.html")

        finally:
            if 'connection' in locals():
                connection.close()
        
    else:
        return redirect(url_for("submission.login"))


@submission.route("/statistics", methods = ["GET"])
@limiter.limit("30 per minute")
def statistics():
    if "user_id" not in session:
        return redirect(url_for("submission.login"))
    
    connection = data_functions.get_connection("prod")
    try:
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

        
        return render_template("stats.html", frontend_data = frontend_data)
    
    except Exception as e:
        print(f"Error: {e}")
        return render_template("error_page.html")

    finally:
        if connection:
            connection.close()

        
    

@submission.route("/delete_user", methods=["GET", "POST"])
@limiter.limit("3 per hour")
def delete_user():
    if "user_id" not in session:
        return redirect(url_for("submission.login"))

    if request.method == "GET":
        return render_template("delete_account.html")

    connection = data_functions.get_connection("prod")
    try:
        user_id = session["user_id"]
        user_info = user_data.fetch_user_id_credentials(connection, user_id)
        input_pw = request.form.get("password")

        if user_info and check_password_hash(user_info[1], input_pw):
            interact_data.delete_user_interactions(connection, user_id)
            cuisine_data.delete_cuisines(connection, user_id)
            user_model_data.delete_user_model(connection, user_id)
            user_data.delete_user(connection, user_id)
            session.clear()
            flash("Account successfully deleted")
        else:
            flash("Incorrect password", "warning")
            return redirect(url_for("submission.delete_user"))

    except Exception as e:
        print(f"Error deleting user: {e}")
        return render_template("error_page.html")

    finally:
        if connection:
            connection.close()

    return redirect(url_for("submission.login"))