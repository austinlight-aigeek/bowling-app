import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base, get_db

# Use SQLite in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Setup TestClient for FastAPI
client = TestClient(app)


# Dependency override for using testing database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def setup_database():
    """
    Setup test database before running tests, and teardown after.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_game(setup_database):
    """
    Test the API endpoint for creating a new game.
    """
    # Correctly structured JSON payload for player_ids
    response = client.post("/games", json={"player_ids": ["player1", "player2"]})
    assert response.status_code == 200
    assert "game_id" in response.json()


def test_invalid_game_id():
    """
    Test retrieving information for a game that doesn't exist.
    """
    response = client.get("/games/nonexistent_game/score")
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


def test_add_roll_to_game(setup_database):
    """
    Test adding a roll to an existing game.
    """
    # First create a game
    response = client.post("/games", json={"player_ids": ["player1", "player2"]})
    assert response.status_code == 200
    game_id = response.json()["game_id"]

    # Add a roll
    roll_response = client.post(f"/games/{game_id}/rolls", json={"pins_knocked": 7})
    assert roll_response.status_code == 200
    assert "current_score" in roll_response.json()


def test_add_invalid_roll(setup_database):
    """
    Test adding an invalid roll (more than 10 pins) to an existing game.
    """
    # First create a game
    response = client.post("/games", json={"player_ids": ["player1", "player2"]})
    game_id = response.json()["game_id"]

    # Add an invalid roll
    roll_response = client.post(f"/games/{game_id}/rolls", json={"pins_knocked": 11})
    assert roll_response.status_code == 422  # Unprocessable Entity (validation error)


def test_get_score(setup_database):
    """
    Test retrieving the current score for a game.
    """
    # Create a game and add rolls
    response = client.post("/games", json={"player_ids": ["player1", "player2"]})
    game_id = response.json()["game_id"]
    client.post(f"/games/{game_id}/rolls", json={"pins_knocked": 7})
    client.post(f"/games/{game_id}/rolls", json={"pins_knocked": 2})

    # Get the current score
    score_response = client.get(f"/games/{game_id}/score")
    assert score_response.status_code == 200
    assert score_response.json()["score"] == 9


def test_get_summary_invalid_game(setup_database):
    """
    Test getting a summary for a game that doesn't exist (edge case).
    """
    response = client.get("/games/invalid_game_id/summary")
    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}
