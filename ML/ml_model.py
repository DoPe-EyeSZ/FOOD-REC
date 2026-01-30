from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from api import api_function
from data import cuisine_data, data_functions, user_data, restaurant_data, interact_data

import pickle
from pathlib import Path

import matplotlib.pyplot as plt

def train_save_model(connection):


    #Gathers all feature data
    feature_data = data_functions.join_interaction_restaurant(connection)
    frequency = api_function.find_frequency(connection)

    #Separates feature data from user response
    features, response = api_function.insert_frequency(feature_data, frequency)

    #CREATE TRAINING SPLIT
    x_train, x_test, y_train, y_test = train_test_split(features, response, test_size=0.2, random_state=42)

    #Scaling feature data so all features are considered equally
    logistic_scaler = StandardScaler()
    x_train_scaled = logistic_scaler.fit_transform(x_train)
    x_test_scaled = logistic_scaler.transform(x_test)

    #LogisticRegression training
    logistic_model = LogisticRegression(max_iter=1000, C=1.0)        
    logistic_model.fit(x_train_scaled, y_train)


    #Saving model and scaler to ML file
    models_dir = Path(__file__).parent.parent / 'ml' / 'models'
    models_dir.mkdir(parents=True, exist_ok=True)

    # Save model
    model_path = models_dir / 'model.pkl'
    pickle.dump(logistic_model, open(model_path, 'wb'))
    print(f"Model saved to {model_path}")

    # Save scaler
    scaler_path = models_dir / 'scaler.pkl'
    pickle.dump(logistic_scaler, open(scaler_path, 'wb'))
    print(f"Scaler saved to {scaler_path}")
    
    score = logistic_model.score(x_test_scaled, y_test)

    return logistic_model, logistic_scaler, score