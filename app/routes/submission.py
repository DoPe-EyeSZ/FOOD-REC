from flask import Blueprint, redirect, url_for, render_template, request, session, flash, jsonify
from data import data_functions
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
        connection = data_functions.get_connection("test_data.db")
        
        #User's Input
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        max_distance = request.form.get("max_distance")

        top10 = reccomendation.get_recs(lat, lng, max_distance, model, scaler, connection)
        if top10 is None:
            connection.close()
            return "Error"
        
        print(top10)
            
        connection.close()    
        return render_template("output.html")
        
        
        
        
    


