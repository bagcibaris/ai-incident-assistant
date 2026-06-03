import joblib

model = joblib.load("models/layer_classifier_model.pkl")

test_logs = [
    "Database Connection Timeout High Application failed to connect to PostgreSQL within 30 seconds",
    "Payment API Timeout High Payment provider did not respond within timeout period",
    "Invalid JWT Token High Request contained expired or invalid JWT token",
    "Disk Full Critical Server disk usage reached 99 percent",
    "Redis Connection Failed High Application failed to connect to Redis cache server",
    "DNS Resolution Failed High Service could not resolve api.payment-provider.com",
    "Null Pointer Exception High Application crashed while accessing user profile object",
    "SQL Injection Attempt Critical Request contained suspicious SQL keywords in input field",
    "Container Restart Loop High Docker container restarted repeatedly within short period",
    "Email Service Failed Medium Password reset email could not be sent"
]

for log in test_logs:
    prediction = model.predict([log])[0]
    probabilities = model.predict_proba([log])[0]
    confidence = max(probabilities)

    print("Log:", log)
    print("Predicted layer:", prediction)
    print("Confidence:", round(confidence, 2))
    print("-" * 70)
