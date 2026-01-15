import os
import requests
from data import cuisine_data, interact_data, restaurant_data


price_levels = {
    "PRICE_LEVEL_FREE": 5,
    "PRICE_LEVEL_INEXPENSIVE": 4,
    "PRICE_LEVEL_MODERATE": 3,
    "PRICE_LEVEL_EXPENSIVE": 2,
    "PRICE_LEVEL_VERY_EXPENSIVE": 1
}

#Extract important data so it can be easily accessable
def extract_api_data(data, connection):
    if "places" in data:

        #Creating the tables 
        cuisine_data.create_cuisine_table(connection)
        restaurant_data.create_restaurant_table(connection)
        interact_data.create_interact_table(connection)

        information = [[],[]]
        for place in data["places"]:

            print(f"\n{'='*60}")
            if "generativeSummary" in place:
                print(f"Summary: {place["generativeSummary"]["overview"]["text"]} \n")

            id = place["id"]
            name = place["displayName"]["text"]

            if "rating" in place:
                rating = place["rating"]
                rating_count = place["userRatingCount"]
                print(f"Rating: {rating}")
                print(f"Rating Count: {rating_count}\n")

            if "priceLevel" in place:
                price_level = price_levels.get(place["priceLevel"], 0)
            else:
                price_level = 0

            print(f"Price: {price_level} \n")

            takeout = 0
            if "takeout" in place:
                if place["takeout"]:
                    takeout = 1
                    print("Allows Takeout")

            dineIn = 0
            if "dineIn" in place:
                if place["dineIn"]:
                    dineIn = 1
                    print("Allows Dine in")

            vegan = 0
            if "servesVegetarianFood" in place:
                if place["servesVegetarianFood"]:
                    vegan = 1
                    print(f"Has Vegitarian Options \n")

            open = 0
            if "currentOpeningHours" in place:
                if "openNow" in place["currentOpeningHours"]:
                    if place["currentOpeningHours"]["openNow"]:
                        open = 1
                        print(f"Currently Open \n")
                    else:
                        print(f"Currently CLOSED \n")

            
            
            resturant = {"id": id, 
                         "name": name, 
                         "rating": rating, 
                         "rating_count": rating_count, 
                         "price_level": price_level, 
                         "takeout":takeout, 
                         "dineIn": dineIn, 
                         "vegan": vegan,
                          "open": open}
            


            #Updates cuisine stats (accepted/shown)
            if "primaryType" in place:
                cuisine = place["primaryType"]
                print(f"Cuisine: {cuisine}")
                resturant["cuisine"] = cuisine
                
            #Add information to restaurnt table
            restaurant_data.insert_restaurant(connection, 
                                              resturant["id"], 
                                              resturant["dineIn"], 
                                              resturant["takeout"], 
                                              resturant["vegan"], 
                                              resturant["price_level"], 
                                              resturant["cuisine"], 
                                              resturant["name"])
            
            information[0].append(resturant)

            #TEST PURPOSES---------------------
            print(f"Name: {name}")
            answer = input("y/n?")

            accept = False

            if answer == "y":
                accept = True

            #-----------------------------
            print(resturant)
            print(f"\n{'='*60}")

            if accept:
                cuisine_data.update_cuisine_stats(connection, cuisine, 1)
                information[1].append(1)
            else:
                cuisine_data.update_cuisine_stats(connection, cuisine, 0)
                information[1].append(0)
        
        #Appends drive time to restaurant info
        for index, value in enumerate(data["routingSummaries"]):
            drive_time = value["legs"][0]["duration"]
            drive_time = drive_time[:len(drive_time)-1]
            information[0][index]["drive_time"] = int(drive_time)

        #Add data to interaction db table
        features = information[0][0]
        response = information[1][0]
        interact_data.insert_interaction(connection,
                                         features["id"],
                                         features["rating"],
                                         features["rating_count"],
                                         features["open"],
                                         features["drive_time"],
                                         response)



    #[[{ID, Name, Rating, Review Count, Price Level, Takeout, Dinein, Vegan, Open?, Drive, Cuisine}], [Accept/Reject]]
    return information      


def find_frequency(connection):       #Find how often user accept/skips food
    cuisine_dict = {}
    cuisine_stats = cuisine_data.fetch_all_cuisine(connection)

    for cuisine in cuisine_stats:
        c = cuisine[0]
        shown = cuisine[1]
        accepted = cuisine[2]
        cuisine_dict[c] = float(float(accepted)/float(shown))

    return cuisine_dict

def insert_frequency(feature_data, freq):       #Insert frequency into cleaned data
    for place_dict in feature_data:
        cuisine = place_dict["cuisine"]
        place_dict["cuisine"] = freq[cuisine]

    return feature_data

def remove_nameid(feature_data):        #Converts all the values of a restaurant to list; remove name/id
    clean_data = []
    for place in feature_data:
        data = list(place.values())
        clean_data.append(data[2:])
    return clean_data


#Calls on API and returns data from fieldmask
def use_api(lat, lng, max_price, max_distance):
    GOOGLE_API_KEY = os.environ.get("google_api_key")
    url = 'https://places.googleapis.com/v1/places:searchNearby'        #Url for Google Places

    distance = round((1609.34 * int(max_distance)), 2)      #Convert from miles to meters
        
    #Returned data from API request
    fields = [
        # Rep and cost
        "places.rating",
        "places.userRatingCount",
        "places.priceLevel",
        
        # Environment
        "places.primaryType",           # Cuisine
        "places.generativeSummary.overview",     # AI summary of review
        
        # Service options
        "places.dineIn",
        "places.takeout",
        "places.servesVegetarianFood",  # Vegan
        
        # Distance (Requires routingParameters in the body)
        "routingSummaries",      # Drive Distance

        #Basic Meta Data
        "places.formattedAddress",
        "places.displayName.text",
        "places.id",
        "places.currentOpeningHours.openNow"
    ]


    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": ",".join(fields)
    }

    params = {
        "maxResultCount": 1,
        "includedPrimaryTypes": ["restaurant"],
        "locationRestriction": {
            "circle": {
            "center": {"latitude": str(lat), "longitude": str(lng)},
            "radius": distance
            }
        },
        "routingParameters": {
            "origin": {
                "latitude": float(lat),
                "longitude": float(lng)
            },
            "travelMode": "DRIVE"
        },
        "minRating": 0.0,

        "priceLevels": [
            "PRICE_LEVEL_FREE",
            "PRICE_LEVEL_INEXPENSIVE",
            "PRICE_LEVEL_MODERATE",
            "PRICE_LEVEL_EXPENSIVE",
            "PRICE_LEVEL_VERY_EXPENSIVE"
        ] 

    }

    return requests.post(url, headers= headers, json=params)