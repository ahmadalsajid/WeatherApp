from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_greetings_without_name():
    response = client.get("/greetings/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
