
#USE FOR DATA COLLECTION

import time
from dotenv import load_dotenv

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from api import api_function
from data import cuisine_data, data_functions, user_data, restaurant_data, interact_data

load_dotenv()

connection = data_functions.get_connection("test")

# SoCal locations with food options (lat, lng, location_name)
location1 = [
    
    (34.0689, -118.4452, "Century City Westfield"),
    (33.7701, -118.1937, "Long Beach Downtown"),
    (34.1478, -118.1445, "Pasadena Old Town"),
    (33.5427, -117.7854, "The Crossroads at Mission Viejo"),
    (33.8366, -117.9143, "The Outlets at Orange"),
    (34.1808, -118.3090, "Universal CityWalk"),
    (33.5950, -117.8620, "Laguna Hills Mall Area"),
    (34.0195, -118.4912, "Santa Monica Third Street Promenade"),
    (33.8303, -118.3416, "Del Amo Fashion Center"),
    (34.1416, -117.9227, "Monrovia Downtown"),
    (33.7175, -117.9542, "The District at Tustin Legacy"),
    (34.0407, -117.5098, "Victoria Gardens, Rancho Cucamonga")
]

location2 = [
    (34.07362, -118.40035, "Beverly Hills Restaurants Area"),            
    (34.04473, -118.24928, "Downtown Los Angeles Food District"),        
    (34.07816, -118.26056, "Echo Park (LA) Food Scene"),                  
    (33.77096, -118.19149, "Long Beach East Village Arts District"),      
    (33.74548, -117.86765, "Anaheim Packing District"),                 
    (33.80454, -117.86534, "Costa Mesa (South Coast Plaza Area)"),     
    (32.71627, -117.16110, "Little Italy, San Diego"),          
    (32.73415, -117.14449, "Hillcrest, San Diego"),          
    (33.98900, -117.37305, "Fullerton Downtown Food Area"),   
    (34.14778, -118.14452, "Pasadena Old Town"),                       
]

location3 = [
    (34.0635, -118.3580, "The Grove, Los Angeles")
]


# Initialize data storage
all_feature_data = []
results = []

# Run 15 API calls
for i in range(len(location3)):
    location = location3[i]
    lat = location[0]
    lng = location[1]
    location_name = location[2]
    max_distance = 5
    
    print(f"\n{'='*60}")
    print(f"Loop {i+1}/{len(location3)}: {location_name}")
    print(f"Coordinates: ({lat}, {lng})")
    print(f"Max Distance: {max_distance} miles")
    print(f"{'='*60}")
    
    response = api_function.use_api(lat, lng, max_distance)
    
    if response.status_code == 200:
        cuisine_data.create_cuisine_table(connection)
        restaurant_data.create_restaurant_table(connection)
        interact_data.create_interact_table(connection)

        data = response.json()
        feature_data = api_function.extract_api_data(data)      #List of dictionaries

        #==================================USER RESPONSE SECTION==================================
        for restaurant in feature_data:
            print("\n==============================")
            print(f"Name: {restaurant['name']}")
            print(f"Rating: {restaurant['rating']}")
            print(f"Number of Reviews: {restaurant['rating_count']}")
            print(f"Price Level (5 == FREE, 1==EXPENSIVE): {restaurant['price_level']}")
            print(f"Takeout Available: {'Yes' if restaurant['takeout'] else 'No'}")
            print(f"Dine-In Available: {'Yes' if restaurant['dineIn'] else 'No'}")
            print(f"Vegan Options: {'Yes' if restaurant['vegan'] else 'No'}")
            print(f"Currently Open: {'Yes' if restaurant['is_open'] else 'No'}")
            print(f"Cuisine Type: {restaurant['cuisine']}")
            print(f"Drive Time: {round(int(restaurant['drive_time'])/60, 2)} minutes")
            print("==============================")

            user_choice = input("Would you accept this restaurant? (y/n): ").strip().lower()

            if user_choice == "y":
                response = 1
                print("Accepted!\n")
            else:
                response = 0
                print("Rejected\n")

            results.append(response)

        #==================================DB STUFF==================================
           
        
            #UPSERTS Restaurant Table
            restaurant_data.insert_restaurant(connection, 
                                              restaurant["id"], 
                                              restaurant["dineIn"], 
                                              restaurant["takeout"], 
                                              restaurant["vegan"], 
                                              restaurant["price_level"], 
                                              restaurant["cuisine"], 
                                              restaurant["name"])

            cuisine_data.upsert_cuisine_stats(connection, restaurant["cuisine"], response)

            interact_data.insert_user_interaction(connection,
                                                restaurant["id"],
                                                restaurant["rating"],
                                                restaurant["rating_count"],
                                                restaurant["is_open"],
                                                restaurant["drive_time"],
                                                response)

                


        
        all_feature_data.extend(feature_data)       #Populated into a list of dictionaries
        print(len(all_feature_data))
        
    else:
        print(f"ERROR {response.status_code}: {response.text}")
    


#=======================================Refine/cleaning data
print(f"\n{'='*60}")
print(f"DATA COLLECTION COMPLETE")
print(f"{'='*60}")


print(f"Total Restaurants Retrieved: {len(all_feature_data)}")
print(f"Total Result Reviewed: {len(results)}")


print(f"Total Interaction Recorded: {len(interact_data.fetch_user_interactions(connection))} \n")


print(f"Total Unique Restaurants: {len(restaurant_data.fetch_restaurants(connection))} \n")


connection.close()