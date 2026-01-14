# test_model.py
import time
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os
from dotenv import load_dotenv
from api import api_function

load_dotenv()
cuisine_stats = {}

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
        info = api_function.extract_api_data(data, cuisine_stats)
        feature_data = info[0]
        results = info[1]
        
        all_feature_data.extend(feature_data)
        result.extend(results)
        
        print(f"Retrieved {len(feature_data)} restaurants")
        print(f"Feature data sample: {feature_data[:2]}")
    else:
        print(f"ERROR {response.status_code}: {response.text}")
    
    if i < 14:
        time.sleep(1)

print(f"\n{'='*60}")
print(f"DATA COLLECTION COMPLETE")
print(f"{'='*60}")
print(f"Total restaurants: {len(all_feature_data)}")
print(f"Total results: {len(result)}")
print(f"Cuisine stats: {cuisine_stats}")

# Process data
print(f"\n{'='*60}")
print("PROCESSING DATA")
print(f"{'='*60}")


frequencies = api_function.find_frequency(cuisine_stats)
print(f"Frequencies: {frequencies}")

update_data = api_function.insert_frequency(all_feature_data, frequencies)
print(f"Frequencies inserted. New data length: {len(update_data)}")
print(f"Sample: {update_data[:3]}")

new_data = api_function.remove_nameid(update_data)
print(new_data)

# Train model
print(f"\n{'='*60}")
print("TRAINING MODEL")
print(f"{'='*60}")

x_train, x_test, y_train, y_test = train_test_split(new_data, result, test_size=0.1, random_state=42)

print(f"Training set: {len(x_train)}")
print(f"Test set: {len(x_test)}")

clf = LinearRegression()
clf.fit(x_train, y_train)

predictions = clf.predict(x_test)
print(f"\nPredictions (first 10): {predictions[:10]}")
print(f"Actual (first 10): {y_test[:10]}")
print(f"Accuracy: {clf.score(x_test, y_test)}")

# VISUALIZATION
print(f"\n{'='*60}")
print("CREATING VISUALIZATIONS")
print(f"{'='*60}")

# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(range(len(y_test)), y_test, label='Actual', alpha=0.6, color='blue')
plt.scatter(range(len(predictions)), predictions, label='Predicted', alpha=0.6, color='red')
plt.axhline(y=0.5, color='green', linestyle='--', label='Decision Boundary (0.5)')
plt.xlabel('Test Sample Index')
plt.ylabel('Value')
plt.title('Predictions vs Actual Values')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
