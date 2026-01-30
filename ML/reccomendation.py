from api import api_function
from data import cuisine_data, data_functions, user_data, restaurant_data, interact_data
import random

from dotenv import load_dotenv
load_dotenv()

def get_recs(lat, long, distance, model, scaler, connection):

    #(1) Grab location/distance from user
    response = api_function.use_api(lat, long, distance)        

    #(2) Check if valid response
    if response.status_code == 200:

        #(3) Converts to json            
        data = response.json()

        #(4) Extract all raw feature data
        feature_data = api_function.extract_api_data(data)        

        #(5) Clean data (remove name/id from feature data)
        clean_feature_data = []        
        for place_dict in feature_data:
                place_id = place_dict["id"]
                name = place_dict["name"]

                dine_in = place_dict["dineIn"]
                takeout = place_dict["takeout"]
                vegan = place_dict["vegan"]
                price_level = place_dict["price_level"]
                cuisine = place_dict["cuisine"]
                rating = place_dict["rating"]
                rating_count = place_dict["rating_count"]
                open = place_dict["is_open"]
                drive = place_dict["drive_time"]

                restaurnt = [dine_in, takeout, vegan, price_level, cuisine, rating, rating_count, open, drive, -1]
                clean_feature_data.append(restaurnt)

                #Updating Restaurant DB     
                #restaurant_data.insert_restaurant(connection, place_id, dine_in, takeout, vegan, price_level, cuisine, name)
                #UPDATE CUISINE TABLE HERE
                #cuisine_data.update_cuisine_stats(connection, cuisine, 0, user_id="test_user") 
                

        #(6) Get frequency dictionary of all cuisines
        frequency_dict = api_function.find_frequency(connection)        

        #(7) insert frequency into feature data
        features, unused = api_function.insert_frequency(clean_feature_data, frequency_dict) 

        #(8) Scale all feature data so no over dominating feature       
        scaled_features = scaler.transform(features)    

        #(9) Predict probability of rejection/acceptance
        prob = model.predict_proba(scaled_features)

        #(10) Pair restaurant with ACCEPTANCE probability; sort from highest to lowest
        sorted_restaurant_prob = sorted(zip(feature_data, prob[:, 1]), key=lambda x: x[1], reverse=True)        

        #(11) Extract highest probability restaurant; select 5 random restaurants for exploration
        top5 = sorted_restaurant_prob[:5]
        bottom15 = sorted_restaurant_prob[5:len(sorted_restaurant_prob)]
        random_5_sample = random.sample(bottom15, min(5, len(bottom15)))
        top10 = top5 + random_5_sample
        random.shuffle(top10)

        #[({feature data}, acceptance probability)]
        return top10
    
    else:
         return None