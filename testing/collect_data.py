
#USE FOR DATA COLLECTION

import time
from dotenv import load_dotenv

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from api import api_function
from data import cuisine_data, data_functions, user_data, restaurant_data, interact_data

load_dotenv()

connection = data_functions.get_connection("test_data.db")

# SoCal locations with food options (lat, lng, location_name)
locations = [
    (34.0381, -117.8648, "The Village at Walnut"),
    (33.9533, -117.7320, "The Shoppes at Chino Hills"),
    (33.6846, -117.8265, "Irvine Spectrum Center"),
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

# Initialize data storage
all_feature_data = []
result = []

# Run 15 API calls
for i in range(len(locations)):
    location = locations[i]
    lat = location[0]
    lng = location[1]
    location_name = location[2]
    max_distance = 5
    
    print(f"\n{'='*60}")
    print(f"Loop {i+1}/{len(locations)}: {location_name}")
    print(f"Coordinates: ({lat}, {lng})")
    print(f"Max Distance: {max_distance} miles")
    print(f"{'='*60}")
    
    response = api_function.use_api(lat, lng, None, max_distance)
    
    if response.status_code == 200:
        data = response.json()
        info = api_function.extract_api_data(data, connection)
        feature_data = info[0]      
        results = info[1]
        
        all_feature_data.extend(feature_data)       #Populated into a list of dictionaries
        result.extend(results)
        
    else:
        print(f"ERROR {response.status_code}: {response.text}")
    


#=======================================Refine/cleaning data
print(f"\n{'='*60}")
print(f"DATA COLLECTION COMPLETE")
print(f"{'='*60}")
print(f"Total restaurants: {len(all_feature_data)}")
print(f"Total results: {len(result)}")

print(f"Cuisine: {cuisine_data.fetch_all_cuisine(connection)}")
#print(f"Total Cuisine: {len(cuisine_data.fetch_all_cuisine(connection))} \n")


#print(f"Interaction: {interact_data.fetch_interactions(connection)}")

print(f"Total Interaction: {len(interact_data.fetch_interactions(connection))} \n")


print(f"Restaurant: {restaurant_data.fetch_restaurants(connection)}")
print(f"Total restaurants: {len(restaurant_data.fetch_restaurants(connection))} \n")


connection.close()