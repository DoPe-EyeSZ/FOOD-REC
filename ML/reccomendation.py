from api import api_function
from data import cuisine_data, data_functions, user_data, restaurant_data, interact_data
import random
import pickle

from dotenv import load_dotenv
load_dotenv()

def get_recs(lat, long, distance, db_location):

    model = pickle.load(open('ml/models/model.pkl', 'rb'))
    scaler = pickle.load(open('ml/models/scaler.pkl', 'rb'))

    #Creating connection/tables
    connection = data_functions.get_connection(db_location)
    cuisine_data.create_cuisine_table(connection)
    user_data.create_user_table(connection)
    restaurant_data.create_restaurant_table(connection)
    interact_data.create_interact_table(connection)

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
                restaurnt = [place_dict["dineIn"], place_dict["takeout"], place_dict["vegan"], place_dict["price_level"],
                            place_dict["cuisine"], place_dict["rating"], place_dict["rating_count"], place_dict["is_open"],
                            place_dict["drive_time"], -1]
                
                #UPSERT RESTAURNT HERE TO DB
                #UPDATE CUISINE TABLE HERE 
                clean_feature_data.append(restaurnt)

        #(6) Get frequency dictionary of all cuisines
        frequency_dict = api_function.find_frequency(connection)        

        #(7) insert frequency into feature data
        features, unused = api_function.insert_frequency(clean_feature_data, frequency_dict) 

        #(8) Scale all feature data so no over dominating feature       
        scaled_features = scaler.transform(features)    

        #(9) Predict probability of rejection/acceptance
        prob = model.predict_proba(scaled_features)

        #(10) Pair restaurant with probability; sort from highest to lowest
        sorted_restaurant_prob = sorted(zip(feature_data, prob[:, 1]), key=lambda x: x[1], reverse=True)        

        #(11) Extract highest probability restaurant; select 5 random restaurants for exploration
        top5 = sorted_restaurant_prob[:5]
        bottom15 = sorted_restaurant_prob[5:len(sorted_restaurant_prob)]
        random_5_sample = random.sample(bottom15, 5)
        top10 = top5 + random_5_sample
        random.shuffle(top10)

        #[({feature data}, probability)]
        return top10

        
        for restaurant in top10:            #(11) show user restaurant

                attributes = restaurant[0]
                prob_accept = restaurant[1]
                print()
                drive_time_minutes = round(attributes["drive_time"] / 60, 1)

                print(f"Name: {attributes['name']}")
                print(f"Rating: {attributes['rating']}")
                print(f"Rating count: {attributes['rating_count']}")
                print(f"Price level: {attributes['price_level']}")
                print(f"Takeout: {attributes['takeout']}")
                print(f"Dine in: {attributes['dineIn']}")
                print(f"Vegan options: {attributes['vegan']}")
                print(f"Open now: {attributes['is_open']}")
                print(f"Cuisine: {attributes['cuisine']}")
                print(f"Drive time: {drive_time_minutes} minutes")

                response = input("Do you like this restaurant? (y/n)")            #(12) save interaction to db

                if response == "y":
                    print("save accept")          #Use userid in session & attributes["place_id"] to find cuisine and update acceptance
                else:
                    print("save rejection")