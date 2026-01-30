import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

import pickle

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from api import api_function
from data import cuisine_data, data_functions, user_data, restaurant_data, interact_data
from ML import reccomendation, ml_model

from dotenv import load_dotenv
load_dotenv()


connection = data_functions.get_connection("test_data.db")

logistic_model, logistic_scaler, score = ml_model.train_save_model(connection)


#LOGISTIC REGRESSION FEATURE IMPORTANCE
print(f"\n{'='*60}")
print("FEATURE IMPORTANCE")
print(f"{'='*60}")

feature_names = ["dine_in", "takeout", "vegan", "price", "cuisine_ratio", "rating", "rating_count", "open", "drive"]

coef = logistic_model.coef_[0]
importance = abs(coef)

sorted_pairs = sorted(zip(feature_names, importance), key=lambda x: x[1], reverse=True)

for name, imp in sorted_pairs:
    bar = '█' * int(imp * 100)
    print(f"{name:15} {imp:.3f} {bar} \n")


# VISUALIZATION
'''print(f"\n{'='*60}")
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
plt.show()'''



#Real world simulation now      (USE AS PIPELINE REFERENCE LATER ON)


'''top10 = reccomendation.get_recs(34.027538, -117.836456, 3, "test_data.db")
      
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
            print("save rejection")'''


connection.close()