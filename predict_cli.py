import joblib

model = joblib.load("models/layer_classifier_model.pkl")

print("AI Incident Response Assistant")
print("Type a log message and I will predict the system layer.")
print("Type 'exit' to quit.")
print("-" * 70)

while True:
    log = input("Enter log: ")

    if log.lower() == "exit":
        print("Exiting assistant...")
        break

    prediction = model.predict([log])[0]
    probabilities = model.predict_proba([log])[0]
    confidence = max(probabilities)

    print("\nPrediction Result")
    print("Predicted layer:", prediction)
    print("Confidence:", round(confidence, 2))
    print("-" * 70)
