from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt


from api import api_function
from data import data_functions

import pickle
from pathlib import Path


def train_save_model(connection, user_id):


    #Gathers all feature data
    feature_data = data_functions.join_interaction_restaurant(connection, user_id)
    frequency = api_function.find_frequency(connection, user_id)


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
        
        
    prediction = logistic_model.predict(x_test_scaled)
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