import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

import random

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from api import api_function
from data import cuisine_data, data_functions, user_data, restaurant_data, interact_data

from dotenv import load_dotenv
load_dotenv()


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

model = LogisticRegression(max_iter=1000, C=1.0)        #LogisticRegression()

model.fit(x_train_scaled, y_train)

prediction = model.predict(x_test_scaled)

score = model.score(x_test_scaled, y_test)

#print(x_test, y_test)
print(f"Accuracy of % {score*100}")

# Cross Validation
scaler2 = StandardScaler()
all_x_scaled = scaler2.fit_transform(features)
cv_scores = cross_val_score(model, all_x_scaled, response, cv=5)
print(f"Accuracy scores of other tests: {cv_scores}")


# Overfitting check
train_score = model.score(x_train_scaled, y_train)
test_score = model.score(x_test_scaled, y_test)
print(f"Train: {train_score:.1%}, Test: {test_score:.1%}, Diff: {abs(train_score-test_score):.1%}")



#Finding feature importance of LOGISTIC REGRESSION
print(f"\n{'='*60}")
print("FEATURE IMPORTANCE")
print(f"{'='*60}")

feature_names = ["dine_in", "takeout", "vegan", "price", "cuisine_ratio", "rating", "rating_count", "open", "drive"]

coef = model.coef_[0]
importance = abs(coef)

sorted_pairs = sorted(zip(feature_names, importance), key=lambda x: x[1], reverse=True)

for name, imp in sorted_pairs:
    bar = '█' * int(imp * 100)
    print(f"{name:15} {imp:.3f} {bar} \n")


'''# VISUALIZATION
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
plt.show()'''



#Real world simulation now      (USE AS PIPELINE REFERENCE LATER ON)

response = api_function.use_api(34.027538, -117.836456, 3)        #(1) Grab location

if response.status_code == 200:        #(2) Check if valid response
        
      data = response.json()         #(3) Converts to json

      feature_data = api_function.extract_api_data(data)        #(4) get all feature data

      clean_feature_data = []        #(5) Clean data to remove name/id form feature data (Join function)
      for place_dict in feature_data:
            restaurnt = [place_dict["dineIn"], place_dict["takeout"], place_dict["vegan"], place_dict["price_level"],
                         place_dict["cuisine"], place_dict["rating"], place_dict["rating_count"], place_dict["is_open"],
                         place_dict["drive_time"], -1]
            clean_feature_data.append(restaurnt)

      frequency_dict = api_function.find_frequency(connection)        #(6) Get frequency of cuisine

      features, response = api_function.insert_frequency(clean_feature_data, frequency_dict)        #(7) insert frequency into feature data
        
      scaled_features = scaler.transform(features)    #(8) Scale all feature data so no over dominating feature
      
      pred = model.predict(scaled_features)        #(9) Predict results

      prob = model.predict_proba(scaled_features)

      print(pred)
      print(prob)

      sorted_restaurant_prob = sorted(zip(feature_data, prob[:, 1]), key=lambda x: x[1], reverse=True)        #(10) sort by highest prob

      top5 = sorted_restaurant_prob[:5]
      bottom15 = sorted_restaurant_prob[5:len(sorted_restaurant_prob)]
      random_5_sample = random.sample(bottom15, 5)
      top10 = top5 + random_5_sample
      print(top10)
      random.shuffle(top10)
      print(top10)





      

      '''for x in range(len(feature_data)):
            prediction = pred[x]
            place = feature_data[x]
            if prediction == 1:
                  print(f"{place["name"]} is predicted to be accepted \n")

            else:
                  print(f"{place["name"]} is predicted to be rejected \n")
'''


connection.close()