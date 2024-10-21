import pytest

# Docstring for the module
"""
This module contains integration tests for the bowling game API endpoints.
It tests the creation of games, recording of rolls, and retrieving the score via API requests.
"""


def test_create_game(client):
    """
    Test the POST /games endpoint to ensure a new game is created successfully.

    Args:
        client (TestClient): The FastAPI test client fixture for making API requests.
    """
    # Make a POST request to create a new game
    response = client.post("/games", json={"player": "Test Player"})

    # Verify that the response is successful and contains the game ID
    assert response.status_code == 200
    data = response.json()
    assert "id" in data


def test_record_roll(client):
    """
    Test the POST /games/{game_id}/rolls endpoint to ensure a roll is recorded correctly.

    Args:
        client (TestClient): The FastAPI test client fixture for making API requests.
    """
    # First, create a new game
    game_response = client.post("/games", json={"player": "Test Player"})
    game_id = game_response.json()["id"]

    # Record a roll in the created game
    roll_response = client.post(f"/games/{game_id}/rolls", json={"pins": 7})

    # Verify that the roll is successfully recorded
    assert roll_response.status_code == 200
    assert roll_response.json() == {"message": "Roll recorded"}


def test_get_score(client):
    """
    Test the GET /games/{game_id}/score endpoint to ensure the correct score is returned.

    Args:
        client (TestClient): The FastAPI test client fixture for making API requests.
    """
    # First, create a new game and record rolls
    game_response = client.post("/games", json={"player": "Test Player"})
    game_id = game_response.json()["id"]

    # Record some rolls
    client.post(f"/games/{game_id}/rolls", json={"pins": 7})
    client.post(f"/games/{game_id}/rolls", json={"pins": 2})

    # Get the score for the game
    score_response = client.get(f"/games/{game_id}/score")

    # Verify the score is calculated correctly (7 + 2 = 9)
    assert score_response.status_code == 200
    assert score_response.json()["score"] == 9


# tests/integration/test_endpoints_edge_cases.py
import pytest


# Test for perfect game
def test_perfect_game_api(client):
    """
    Test creating a perfect game via the API (12 strikes, score of 300).
    """
    response = client.post("/games", json={"player": "Perfect Player"})
    game_id = response.json()["id"]

    # Simulate 12 strikes
    for _ in range(12):
        client.post(f"/games/{game_id}/rolls", json={"pins": 10})

    score_response = client.get(f"/games/{game_id}/score")
    assert score_response.status_code == 200
    assert score_response.json()["score"] == 300


# Test for gutter game
def test_gutter_game_api(client):
    """
    Test creating a gutter game via the API (0 pins on every roll, score of 0).
    """
    response = client.post("/games", json={"player": "Gutter Player"})
    game_id = response.json()["id"]

    # Simulate gutter game
    for _ in range(10):
        client.post(f"/games/{game_id}/rolls", json={"pins": 0})
        client.post(f"/games/{game_id}/rolls", json={"pins": 0})

    score_response = client.get(f"/games/{game_id}/score")
    assert score_response.status_code == 200
    assert score_response.json()["score"] == 0


# Test for spare calculation
def test_spare_game_api(client):
    """
    Test spare calculation via the API (spare followed by a regular roll).
    """
    response = client.post("/games", json={"player": "Spare Player"})
    game_id = response.json()["id"]

    # Simulate a spare and a regular roll
    client.post(f"/games/{game_id}/rolls", json={"pins": 5})
    client.post(f"/games/{game_id}/rolls", json={"pins": 5})  # Spare
    client.post(f"/games/{game_id}/rolls", json={"pins": 3})

    score_response = client.get(f"/games/{game_id}/score")
    assert score_response.status_code == 200
    assert score_response.json()["score"] == 16  # (5 + 5 + 3) + 3 = 16


# Test for invalid roll API request
def test_invalid_roll_api(client):
    """
    Test that invalid rolls (negative or too many pins) return the appropriate error.
    """
    response = client.post("/games", json={"player": "Invalid Player"})
    game_id = response.json()["id"]

    # Attempt to send an invalid roll
    roll_response = client.post(f"/games/{game_id}/rolls", json={"pins": -1})
    assert roll_response.status_code == 400
    assert "invalid roll" in roll_response.json()["detail"].lower()
