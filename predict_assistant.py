import joblib

model = joblib.load("models/layer_classifier_model.pkl")

LAYER_RESPONSES = {
    "Application Layer": {
        "severity": "Medium/High",
        "probable_cause": "Application code error, invalid input, missing validation, or unhandled exception.",
        "suggested_action": "Check application logs, stack trace, request payload, validation rules, and exception handling."
    },
    "Database Layer": {
        "severity": "High",
        "probable_cause": "Database connection issue, slow query, deadlock, migration error, or storage problem.",
        "suggested_action": "Check database health, connection pool, query performance, indexes, locks, and disk usage."
    },
    "Network Layer": {
        "severity": "High",
        "probable_cause": "DNS failure, connection timeout, gateway issue, firewall problem, or unstable network route.",
        "suggested_action": "Check DNS settings, service availability, firewall rules, load balancer health, and network latency."
    },
    "Infrastructure Layer": {
        "severity": "High/Critical",
        "probable_cause": "Server resource exhaustion, container crash, disk full, memory pressure, or failed health check.",
        "suggested_action": "Check CPU, RAM, disk usage, container logs, system logs, service status, and health checks."
    },
    "Security Layer": {
        "severity": "High/Critical",
        "probable_cause": "Unauthorized access attempt, invalid token, brute-force attack, injection attempt, or suspicious activity.",
        "suggested_action": "Block suspicious requests, inspect authentication logs, rotate exposed secrets, and review access control rules."
    },
    "Cache Layer": {
        "severity": "Medium/High",
        "probable_cause": "Redis/cache connection failure, stale data, cache invalidation issue, memory limit, or cache stampede.",
        "suggested_action": "Check Redis status, memory usage, TTL settings, invalidation rules, and cache key generation strategy."
    },
    "External Service Layer": {
        "severity": "Medium/High",
        "probable_cause": "Third-party API timeout, payment provider failure, email/SMS provider issue, or invalid external credentials.",
        "suggested_action": "Check external provider status, API credentials, retry policy, timeout settings, and fallback mechanism."
    }
}

print("AI Incident Response Assistant")
print("Type a log message and I will predict the system layer and suggest an action.")
print("Type 'exit' to quit.")
print("-" * 80)

while True:
    log = input("Enter log: ")

    if log.lower() == "exit":
        print("Exiting assistant...")
        break

    prediction = model.predict([log])[0]
    probabilities = model.predict_proba([log])[0]
    confidence = max(probabilities)

    response = LAYER_RESPONSES.get(prediction, {
        "severity": "Unknown",
        "probable_cause": "No probable cause found.",
        "suggested_action": "No suggested action found."
    })

    print("\nIncident Analysis Result")
    print("Predicted layer:", prediction)
    print("Confidence:", round(confidence, 2))
    print("Estimated severity:", response["severity"])
    print("Probable cause:", response["probable_cause"])
    print("Suggested action:", response["suggested_action"])
    print("-" * 80)
