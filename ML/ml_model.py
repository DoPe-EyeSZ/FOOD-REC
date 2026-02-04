from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from api import api_function
from data import data_functions

import pickle
from pathlib import Path


def train_save_model(connection):


    #Gathers all feature data
    feature_data = data_functions.join_interaction_restaurant(connection)
    frequency = api_function.find_frequency(connection)


    #Separates feature data from user response
    features, response = api_function.insert_frequency(feature_data, frequency)


    #Create training split
    x_train, x_test, y_train, y_test = train_test_split(features, response, test_size=0.2, random_state=42)


    #Scaling feature data so all features are considered equally
    logistic_scaler = StandardScaler()
    x_train_scaled = logistic_scaler.fit_transform(x_train)
    x_test_scaled = logistic_scaler.transform(x_test)


    #LogisticRegression training
    logistic_model = LogisticRegression(max_iter=1000, C=1.0)        
    logistic_model.fit(x_train_scaled, y_train)
    
    
    #Get Accuracy Score
    score = logistic_model.score(x_test_scaled, y_test)
    print(f"Model is {round(score * 100, 2)}% accurate \n")


    #Cross validation on new model
    scaler2 = StandardScaler()
    all_x_scaled = scaler2.fit_transform(features)
    cv_scores = cross_val_score(LogisticRegression(max_iter=1000, C=1.0), all_x_scaled, response, cv=5)
    print(f"Accuracy scores of other tests: {cv_scores} \n")


    #Check for overfitting
    train_score = logistic_model.score(x_train_scaled, y_train)
    test_score = logistic_model.score(x_test_scaled, y_test)
    print(f"Train: {train_score:.1%}, Test: {test_score:.1%}, Diff: {abs(train_score-test_score):.1%} \n")

    answer = input("Do you want to save model? (yes/no): ").lower()

    if answer == "yes":
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

        print("Save complete!")

    

    return logistic_model, logistic_scaler, score