from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["platform"] == "Kubernetes"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_hello():
    response = client.get("/api/v1/hello/Manoharan")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Manoharan!"}
