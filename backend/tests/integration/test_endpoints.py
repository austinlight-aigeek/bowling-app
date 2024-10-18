# backend/tests/integration/test_endpoints.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_game():
    response = client.post("/games")
    assert response.status_code == 200
    assert "game_id" in response.json()


def test_record_roll():
    response = client.post("/games")
    game_id = response.json()["game_id"]

    response = client.post(f"/games/{game_id}/rolls", json={"pins": 5})
    assert response.status_code == 200
    assert response.json()["roll"] == 5


def test_get_score():
    response = client.post("/games")
    game_id = response.json()["game_id"]

    client.post(f"/games/{game_id}/rolls", json={"pins": 10})  # Strike
    response = client.get(f"/games/{game_id}/score")
    assert response.status_code == 200
    assert "score" in response.json()


def test_summary():
    response = client.post("/games")
    game_id = response.json()["game_id"]

    client.post(f"/games/{game_id}/rolls", json={"pins": 10})  # Strike
    response = client.get(f"/games/{game_id}/summary")
    assert response.status_code == 200
    assert "summary" in response.json()
