import pytest


@pytest.mark.usefixtures("setup_database")
def test_create_game(client):
    """
    Test the API endpoint for creating a new game.
    """
    # Correctly structured JSON payload with player_name
    response = client.post("/games", json={"player_name": "Player One"})

    assert response.status_code == 200
    assert "game_id" in response.json()
    assert "player_id" in response.json()  # Check that the player_id is returned
    assert response.json()["player_name"] == "Player One"


def test_invalid_game_id(client):
    """
    Test retrieving information for a game that doesn't exist.
    """
    response = client.get("/games/nonexistent_game/score")
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


@pytest.mark.usefixtures("setup_database")
def test_add_roll_to_game(client):
    """
    Test adding a roll to an existing game.
    """
    # First create a game
    response = client.post("/games", json={"player_name": "Player Two"})
    assert response.status_code == 200
    game_id = response.json()["game_id"]

    # Add a roll
    roll_response = client.post(f"/games/{game_id}/rolls", json={"pins_knocked": 7})
    assert roll_response.status_code == 200
    assert "current_score" in roll_response.json()


@pytest.mark.usefixtures("setup_database")
def test_add_invalid_roll(client):
    """
    Test adding an invalid roll (more than 10 pins) to an existing game.
    """
    # First create a game
    response = client.post("/games", json={"player_name": "Player Three"})
    game_id = response.json()["game_id"]

    # Add an invalid roll
    roll_response = client.post(f"/games/{game_id}/rolls", json={"pins_knocked": 11})
    assert roll_response.status_code == 422  # Unprocessable Entity (validation error)


@pytest.mark.usefixtures("setup_database")
def test_get_score(client):
    """
    Test retrieving the current score for a game.
    """
    # Create a game and add rolls
    response = client.post("/games", json={"player_name": "Player Four"})
    game_id = response.json()["game_id"]
    client.post(f"/games/{game_id}/rolls", json={"pins_knocked": 7})
    client.post(f"/games/{game_id}/rolls", json={"pins_knocked": 2})

    # Get the current score
    score_response = client.get(f"/games/{game_id}/score")
    assert score_response.status_code == 200
    assert score_response.json()["score"] == 9


@pytest.mark.usefixtures("setup_database")
def test_get_summary_invalid_game(client):
    """
    Test getting a summary for a game that doesn't exist (edge case).
    """
    response = client.get("/games/invalid_game_id/summary")
    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}
