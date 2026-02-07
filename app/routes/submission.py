from flask import Blueprint, redirect, url_for, render_template, request, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from data import data_functions, interact_data, cuisine_data, user_data
from ML import reccomendation
import pickle


from dotenv import load_dotenv
load_dotenv()



submission = Blueprint("submission", __name__, template_folder="templates")
model = pickle.load(open('ml/models/model.pkl', 'rb'))
scaler = pickle.load(open('ml/models/scaler.pkl', 'rb'))


@submission.route("/", methods = ["POST", "GET"])
@submission.route("/login", methods = ["POST", "GET"])
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
            return render_template("login.html")


    return render_template("login.html")


@submission.route("/logout", methods = ["GET"])
def logout():
    if "user_id" in session:
        session.clear()
        flash("Successfully logged out!", "success")
    
    else:
        flash("You're not logged in", "warning")

    return render_template("login.html")



@submission.route("/signup", methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        connection = data_functions.get_connection("prod")

        if not user_data.fetch_user_credentials(connection, username):
            pw_hash = generate_password_hash(password)
            user_data.create_user(connection, username, pw_hash)
            user_id = user_data.fetch_user_credentials(connection, username)[0]
            session["user_id"] = user_id
            flash("user created")
            return redirect(url_for("submission.user_submission"))

        else:
            flash("Username already exists", "warning")
            return render_template("signup.html")

    else:
        return render_template("signup.html")


#@submission.route("/", methods = ["POST", "GET"])
@submission.route("/user_submission", methods = ["POST", "GET"])
def user_submission():
    print(session)
    if session["user_id"]:
        if request.method == "GET":     #For after user logs in
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
                return "Error"
            
            session["suggestions"] = top10
            print(session["suggestions"])
            session["index"] = 0
                
            connection.close()    
            return redirect(url_for("submission.show_restaurant"))
    
    else:
        render_template("login.html")
    

@submission.route("/show_restaurant")
def show_restaurant():
    if session["user_id"]:
        suggestions = session["suggestions"]
        index = session["index"]

        restaurant_to_display = suggestions[index]
        
        return render_template("display_restaurant.html", displayed_restaurant = restaurant_to_display)
    
    else:
        render_template("login.html")


@submission.route("/process_response", methods = ["POST"])
def process_response():
    if session["user_id"]:
        connection = data_functions.get_connection("prod")
        session["index"] += 1
        
        response = request.form.get("response")
        place_id = request.form.get("place_id")
        cuisine = request.form.get("cuisine")
        rating = request.form.get("rating")
        rating_count = request.form.get("rating_count")
        opening = request.form.get("is_open")
        drive_time = request.form.get("drive_time")

        #Saving interaction
        interact_data.insert_user_interaction(connection, 
                                              place_id, 
                                              rating, 
                                              rating_count, 
                                              opening, 
                                              drive_time, 
                                              response, 
                                              user_id=session["user_id"])

        #Increment acceptance
        if response == "1":
            cuisine_data.increment_acceptance(connection, 
                                              cuisine, 
                                              user_id = session["user_id"])


        if session["index"] < len(session["suggestions"]):
            connection.close()
            return redirect(url_for("submission.show_restaurant"))
        
        else:
            reccent_10 = data_functions.join_10_restaurant(connection, user_id = session["user_id"])
            connection.close()
            return render_template("summary.html", displayed_restaurants = reccent_10)
        
    else:
        render_template("login.html")

        
        
        
        
    


