import joblib
import pandas as pd

# Load trained model
model = joblib.load("models/machine_model.pkl")


def predict_status(temperature, vibration, pressure, rpm):

    data = pd.DataFrame({
        "Temperature": [temperature],
        "Vibration": [vibration],
        "Pressure": [pressure],
        "RPM": [rpm]
    })

    prediction = model.predict(data)

    return prediction[0]