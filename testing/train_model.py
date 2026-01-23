import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from api import api_function
from data import cuisine_data, data_functions, user_data, restaurant_data, interact_data

connection = data_functions.get_connection("test_data.db")

'''print(f"Cuisine: {cuisine_data.fetch_all_cuisine(connection)}")
print(f"Total Cuisine: {len(cuisine_data.fetch_all_cuisine(connection))} \n")


print(f"Interaction: {interact_data.fetch_interactions(connection)}")
print(f"Total Interaction: {len(interact_data.fetch_interactions(connection))} \n")


print(f"Restaurant: {restaurant_data.fetch_restaurants(connection)}")
print(f"Total restaurants: {len(restaurant_data.fetch_restaurants(connection))} \n")'''

#Gathers needed data
feature_data = data_functions.join_interaction_restaurant(connection)
frequency = api_function.find_frequency(connection)

#Separates feature data from user response
features, response = api_function.insert_frequency(feature_data, frequency)

#Creating test data/ model
x_train, x_test, y_train, y_test = train_test_split(features, response, test_size=0.2, random_state=42)

#Scaling feature data so all features are considered equally
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

model = LogisticRegression()

model.fit(x_train_scaled, y_train)

prediction = model.predict(x_test_scaled)

score = model.score(x_test_scaled, y_test)

#print(x_test, y_test)
print(prediction)
print(score)


# VISUALIZATION
print(f"\n{'='*60}")
print("CREATING VISUALIZATIONS")
print(f"{'='*60}")

# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(range(len(y_test)), y_test, label='Actual', alpha=0.6, color='blue')
plt.scatter(range(len(prediction)), prediction, label='Predicted', alpha=0.6, color='red')
plt.axhline(y=0.5, color='green', linestyle='--', label='Decision Boundary (0.5)')
plt.xlabel('Test Sample Index')
plt.ylabel('Value')
plt.title('Predictions vs Actual Values')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


connection.close()