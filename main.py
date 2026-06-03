import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


model = joblib.load("models/layer_classifier_model.pkl")


app = FastAPI(
    title="AI Incident Response Assistant",
    description="Predicts incident layer and suggests probable cause/action from log messages.",
    version="1.1.0"
)


class LogRequest(BaseModel):
    log: str


class BatchLogRequest(BaseModel):
    logs: List[str]


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


def analyze_log(log: str):
    prediction = model.predict([log])[0]

    probabilities = model.predict_proba([log])[0]
    confidence = float(max(probabilities))

    response = LAYER_RESPONSES.get(prediction, {
        "severity": "Unknown",
        "probable_cause": "No probable cause found.",
        "suggested_action": "No suggested action found."
    })

    return {
        "input_log": log,
        "predicted_layer": prediction,
        "confidence": round(confidence, 2),
        "estimated_severity": response["severity"],
        "probable_cause": response["probable_cause"],
        "suggested_action": response["suggested_action"]
    }


@app.get("/")
def root():
    return {
        "message": "AI Incident Response Assistant API is running",
        "version": "1.1.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "service": "AI Incident Response Assistant"
    }


@app.get("/layers")
def get_layers():
    return {
        "supported_layers": list(LAYER_RESPONSES.keys())
    }


@app.post("/predict")
def predict_incident(request: LogRequest):
    return analyze_log(request.log)


@app.post("/predict/batch")
def predict_batch(request: BatchLogRequest):
    results = []

    for log in request.logs:
        results.append(analyze_log(log))

    return {
        "total_logs": len(request.logs),
        "results": results
    }
