import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load dataset
data = pd.read_csv("data/training_data.csv")

# Input Features
X = data[["Temperature", "Vibration", "Pressure", "RPM"]]

# Output Label
y = data["Status"]

# Create AI Model
model = DecisionTreeClassifier(random_state=42)

# Train Model
model.fit(X, y)

# Save Model
joblib.dump(model, "models/machine_model.pkl")

print("=" * 50)
print("AI Model Trained Successfully!")
print("Model saved as models/machine_model.pkl")
print("=" * 50)