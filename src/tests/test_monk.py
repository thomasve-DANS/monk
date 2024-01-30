#!/usr/bin/env python3
from fastapi.testclient import TestClient

from main import app

client = TestClient(app=app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"Magic": "Begins here"}
    wrong_post = client.post('/')
    assert wrong_post.status_code == 405

def test_log():
    payload = {
        "message": {
            "monkey": "test",
            "number": 3,
        },
        "propagation_id": 1,
        "level": "critical",
    }
    response = client.post("/log", data=payload)
    print(response.json())
    assert response.status_code == 200
    assert "timestamp" in response.json()
    assert response.json()["message"]["monkey"] == "test"
    assert response.json()["message"]["number"] == 3
    assert response.json()["propagation_id"] == 1
    assert response.json()["level"] == "warning"
    del payload["status"]
    response = client.post("/log", data=payload)
    assert response.json()["level"] == "info"
