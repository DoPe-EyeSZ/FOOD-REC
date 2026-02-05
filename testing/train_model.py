import matplotlib.pyplot as plt

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from data import data_functions
from ML import ml_model

from dotenv import load_dotenv
load_dotenv()


connection = data_functions.get_connection("test")

logistic_model, logistic_scaler, score = ml_model.train_save_model(connection, user_id=1)


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




connection.close()