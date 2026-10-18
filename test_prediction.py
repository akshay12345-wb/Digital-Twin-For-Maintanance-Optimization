from ai.prediction import predict_status

status = predict_status(
    temperature=82,
    vibration=6.5,
    pressure=7.0,
    rpm=1450
)

print("=" * 40)
print("AI Prediction")
print("=" * 40)
print("Predicted Status :", status)