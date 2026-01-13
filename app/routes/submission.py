from flask import Blueprint, redirect, url_for, render_template, request, session, flash, jsonify
from sklearn.model_selection import train_test_split
import json
from api import api_function



submission = Blueprint("submission", __name__, template_folder="templates")


cuisine_stats = {}


@submission.route("/", methods = ["POST", "GET"])
def user_submission():
    if request.method == "GET":     #For after user logs in
        return render_template("submission.html")
    
    else:

        #User's request/data
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        max_price = request.form.get("max_price")
        max_distance = request.form.get("max_distance")

        response = api_function.use_api(lat, lng, max_price, max_distance)

        if response.status_code == 200:

            
            data = response.json()
            info = api_function.extract_api_data(data, cuisine_stats)        #[[Feature data], [Acceptances/Rejections]]
            all_feature_data = info[0]
            result = info[1]

            clean_feature_data = api_function.remove_id(all_feature_data)        #Removes id from index 0

            frequencies = api_function.find_frequency(cuisine_stats)     #Calculates ratio of acceptances/rejections
            
            new_data = api_function.insert_frequency(clean_feature_data, frequencies)        #Replaces ratio of accept/reject into clean data

            x_train, x_test, y_train, y_test = train_test_split(new_data, result, test_size=0.2)
            from sklearn.linear_model import LinearRegression
            clf = LinearRegression()
            clf.fit(x_train, y_train)
            print(clf.predict(x_test))
            print(y_test)
            print(f"Accuracy: {clf.score(x_test, y_test)}")
            
            return render_template("output.html")
        

        else:

            print(f"Error {response.status_code}: {response.text}")
            return redirect(request.referrer)
        
        
        
    


