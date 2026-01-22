import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from api import api_function
from data import cuisine_data, data_functions, user_data, restaurant_data, interact_data

connection = data_functions.get_connection("test_data.db")

feature_data = data_functions.join_interaction_restaurant(connection)
frequency = api_function.find_frequency(connection)

features, response = api_function.insert_frequency(feature_data, frequency)

print(f"FEATURE DATA: {features} \n")
print(f"UPDATED DATA: {response} \n")
print(f"FREQUENCY DATA: {frequency} \n")


'''
update_data = api_function.insert_frequency(all_feature_data, frequencies)
print(f"Frequencies inserted. New data length: {len(update_data)}")
print(f"Sample: {update_data[:3]}")

new_data = api_function.remove_nameid(update_data)
print(new_data)

# ======================================================================Train model
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
'''


connection.close()