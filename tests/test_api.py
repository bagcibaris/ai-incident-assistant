import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["service"] == "AI Incident Response Assistant"


def test_get_layers():
    response = client.get("/layers")

    assert response.status_code == 200

    data = response.json()
    assert "supported_layers" in data
    assert "Application Layer" in data["supported_layers"]
    assert "Database Layer" in data["supported_layers"]
    assert "Security Layer" in data["supported_layers"]
    assert "Cache Layer" in data["supported_layers"]


def test_predict_single_log():
    payload = {
        "log": "Redis memory limit was reached and application cannot store cache keys"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["input_log"] == payload["log"]
    assert data["predicted_layer"] == "Cache Layer"
    assert "confidence" in data
    assert "estimated_severity" in data
    assert "probable_cause" in data
    assert "suggested_action" in data


def test_predict_security_log():
    payload = {
        "log": "Multiple failed login attempts detected from same IP address"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["predicted_layer"] == "Security Layer"


def test_predict_batch_logs():
    payload = {
        "logs": [
            "Redis memory limit was reached and application cannot store cache keys",
            "Multiple failed login attempts detected from same IP address",
            "Payment provider returned 502 error during checkout",
            "PostgreSQL query took 15 seconds to complete during product search",
            "Docker container restarted repeatedly after deployment"
        ]
    }

    response = client.post("/predict/batch", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["total_logs"] == 5
    assert len(data["results"]) == 5

    predicted_layers = [item["predicted_layer"] for item in data["results"]]

    assert "Cache Layer" in predicted_layers
    assert "Security Layer" in predicted_layers
    assert "External Service Layer" in predicted_layers
    assert "Database Layer" in predicted_layers
    assert "Infrastructure Layer" in predicted_layers
