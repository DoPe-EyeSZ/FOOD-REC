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
def extract_api_data(data):
    if "places" in data:


        info = []
        for place in data["places"]:

            #if "generativeSummary" in place:
                #print(f"Summary: {place["generativeSummary"]["overview"]["text"]} \n")

            id = place["id"]

            name = place["displayName"]["text"]

            rating = place.get("rating", 0)

            rating_count = place.get("userRatingCount", 0)

            price_level = price_levels.get(place.get("priceLevel", 0))

            takeout = 1 if place.get("takeout", False) else 0

            dineIn = 1 if place.get("dineIn", False) else 0

            vegan = 1 if place.get("servesVegetarianFood", False) else 0

            open = 1 if place.get("currentOpeningHours", {}).get("openNow", False) else 0

            cuisine = place.get("primaryType", "restaurant") 



            restaurant = {"id": id, 
                         "name": name, 
                         "rating": rating, 
                         "rating_count": rating_count, 
                         "price_level": price_level, 
                         "takeout":takeout, 
                         "dineIn": dineIn, 
                         "vegan": vegan,
                         "is_open": open,
                         "cuisine": cuisine}
            
            info.append(restaurant)
            
                
        #Appends drive time to restaurant info
        for index, value in enumerate(data["routingSummaries"]):

            drive_time = value["legs"][0]["duration"]
            drive_time = drive_time[:len(drive_time)-1]
            info[index]["drive_time"] = int(drive_time)



    #[{ID, Name, Rating, Review Count, Price Level, Takeout, Dinein, Vegan, Open?, Drive, Cuisine},
    #{ID, Name, Rating, Review Count, Price Level, Takeout, Dinein, Vegan, Open?, Drive, Cuisine}]
    return info      


def find_frequency(connection):       #Find how often user accept/skips food
    cuisine_dict = {}
    cuisine_stats = cuisine_data.fetch_all_cuisine(connection)

    for cuisine in cuisine_stats:
        c = cuisine[1]
        shown = cuisine[2]
        accepted = cuisine[3]
        cuisine_dict[c] = float(float(accepted)/float(shown))

    return cuisine_dict

def insert_frequency(feature_data, freq_dict):       #Insert frequency into cleaned data
    features = []
    user_response = []

    for place in feature_data:
        restaurant = list(place)

        #Replaces cuisine w frequency
        restaurant[4] = freq_dict[restaurant[4]]        
        features.append(restaurant[:len(restaurant)-1])
        user_response.append(restaurant[-1])

    return features, user_response


def remove_nameid(feature_data):        #Converts all the values of a restaurant to list; remove name/id
    clean_data = []
    for place in feature_data:
        data = list(place.values())
        clean_data.append(data[2:])
    return clean_data


#Calls on API and returns data from fieldmask
def use_api(lat, lng, max_distance):
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
        "maxResultCount": 20,
        "includedPrimaryTypes": ["restaurant", "cafe", "bar", "fast_food_restaurant", "coffee_shop"],
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