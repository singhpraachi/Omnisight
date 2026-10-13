
from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "OmniSight API",
    }


def test_valid_webhook():
    payload = {
        "event": "deployment_completed",
        "repository": "OmniSight",
        "build_id": "build-123",
        "url": "https://example.com",
    }

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == "received"
    assert response.json()["repository"] == "OmniSight"


def test_invalid_webhook_url():
    payload = {
        "event": "deployment_completed",
        "repository": "OmniSight",
        "build_id": "build-123",
        "url": "not-a-valid-url",
    }

    response = client.post("/webhook", json=payload)

    assert response.status_code == 422


def test_missing_required_field():
    payload = {
        "event": "deployment_completed",
        "repository": "OmniSight",
        "url": "https://example.com",
    }

    response = client.post("/webhook", json=payload)

    assert response.status_code == 422
