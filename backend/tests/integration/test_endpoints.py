import pytest
from fastapi.testclient import TestClient
from app.db import models
from sqlalchemy.orm import Session


def test_create_game(client: TestClient):
    """
    Test creating a new bowling game.

    This test ensures that a game can be created with a valid player name.
    """
    # Arrange
    data = {"player": "John Doe"}

    # Act
    response = client.post("/games", json=data)

    # Assert
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["player"] == "John Doe"
    assert "id" in response_json  # Ensure the game ID is returned


def test_create_game_missing_player(client: TestClient):
    """
    Test creating a new game without providing a player name.

    This should return a 422 Unprocessable Entity status as the player name is required.
    """
    # Act
    response = client.post("/games", json={})

    # Assert
    assert response.status_code == 422  # Missing required field (player name)


def test_record_roll_valid(client: TestClient, db: Session):
    """
    Test recording valid rolls for a specific game.

    This test ensures that rolls can be recorded and updated for a valid game.
    """
    # Arrange
    game = models.Game(player="Test Player")
    db.add(game)
    db.commit()
    db.refresh(game)

    data = {
        "frames": [[7, 3], [10], [6, 2]]
    }  # Frame 1: Spare, Frame 2: Strike, Frame 3: Open frame

    # Act
    response = client.post(f"/games/{game.id}/rolls", json=data)

    # Assert
    assert response.status_code == 200
    assert response.json() == "Rolls recorded successfully."


def test_record_roll_invalid_game_id(client: TestClient):
    """
    Test recording rolls for an invalid game ID.

    This should return a 404 error because the game does not exist.
    """
    # Arrange
    invalid_game_id = 99999
    data = {"frames": [[7, 3], [10], [6, 2]]}

    # Act
    response = client.post(f"/games/{invalid_game_id}/rolls", json=data)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


def test_get_score_strike_spare_open_frame(client: TestClient, db: Session):
    """
    Test calculating the score with a combination of strike, spare, and open frame.

    - Frame 1: Strike (10 points + next two rolls)
    - Frame 2: Spare (5 + 5 points + next roll)
    - Frame 3: Open frame (4 + 3 points)
    Expected total score: 41
    """
    # Arrange
    game = models.Game(player="Test Player")
    db.add(game)
    db.commit()
    db.refresh(game)

    frames = [
        [10],
        [5, 5],
        [4, 3],
    ]  # Strike (frame 1)  # Spare (frame 2)  # Open frame (frame 3)

    # Record the rolls
    for i, frame_rolls in enumerate(frames):
        frame = models.Frame(game_id=game.id, frame_number=i + 1, rolls=frame_rolls)
        db.add(frame)
    db.commit()

    # Act
    response = client.get(f"/games/{game.id}/score")

    # Assert
    # Score calculation: 20 (frame 1) + 14 (frame 2) + 7 (frame 3) = 41
    assert response.status_code == 200
    assert response.json()["score"] == 41


def test_get_score_tenth_frame_strike(client: TestClient, db: Session):
    """
    Test calculating the score with strikes in all frames, including the 10th frame.

    In the 10th frame, the player gets two bonus rolls after a strike.
    This should result in a perfect game with a score of 300.
    """
    # Arrange
    game = models.Game(player="Test Player")
    db.add(game)
    db.commit()
    db.refresh(game)

    # All strikes, including 10th frame with two bonus rolls
    frames = [
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [10, 10, 10],  # 10th frame: Strike + two bonus rolls
    ]

    # Record the rolls
    for i, frame_rolls in enumerate(frames):
        frame = models.Frame(game_id=game.id, frame_number=i + 1, rolls=frame_rolls)
        db.add(frame)
    db.commit()

    # Act
    response = client.get(f"/games/{game.id}/score")

    # Assert
    # Perfect game score = 300
    assert response.status_code == 200
    assert response.json()["score"] == 300


def test_get_score_tenth_frame_spare(client: TestClient, db: Session):
    """
    Test calculating the score with spares and strikes, including a spare in the 10th frame.

    In the 10th frame, the player gets one bonus roll after a spare.
    Expected total score: 275.
    """
    # Arrange
    game = models.Game(player="Test Player")
    db.add(game)
    db.commit()
    db.refresh(game)

    # Strikes in frames 1-9, spare in 10th frame with one bonus roll
    frames = [
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [5, 5, 10],
    ]  # 10th frame: Spare + one bonus roll

    # Record the rolls
    for i, frame_rolls in enumerate(frames):
        frame = models.Frame(game_id=game.id, frame_number=i + 1, rolls=frame_rolls)
        db.add(frame)
    db.commit()

    # Act
    response = client.get(f"/games/{game.id}/score")

    # Assert
    # Total score = 275
    assert response.status_code == 200
    assert response.json()["score"] == 275


def test_get_score_tenth_frame_open(client: TestClient, db: Session):
    """
    Test calculating the score when the player has an open frame in the 10th frame.

    The player does not get bonus rolls if they don't knock all pins down in the 10th frame.
    Expected total score: 267.
    """
    # Arrange
    game = models.Game(player="Test Player")
    db.add(game)
    db.commit()
    db.refresh(game)

    # Strikes in frames 1-9, open frame in 10th
    frames = [
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [10],
        [4, 3],
    ]  # 10th frame: Open frame

    # Record the rolls
    for i, frame_rolls in enumerate(frames):
        frame = models.Frame(game_id=game.id, frame_number=i + 1, rolls=frame_rolls)
        db.add(frame)
    db.commit()

    # Act
    response = client.get(f"/games/{game.id}/score")

    # Assert
    # Total score = 267
    assert response.status_code == 200
    assert response.json()["score"] == 267


def test_get_summary_valid(client: TestClient, mocker):
    """
    Test generating a natural language summary of the game using an LLM.

    This test mocks the LLM to ensure the summary is generated correctly and returned via the summary endpoint.
    """
    # Mock the LLM summary generation
    mocker.patch("app.api.llm.get_llm_summary", return_value="Test summary")

    # Arrange
    game = models.Game(player="Test Player")
    db.add(game)
    db.commit()
    db.refresh(game)

    frame = models.Frame(game_id=game.id, frame_number=1, rolls=[5, 4])
    db.add(frame)
    db.commit()

    # Act
    response = client.get(f"/games/{game.id}/summary")

    # Assert
    assert response.status_code == 200
    assert response.json()["summary"] == "Test summary"


def test_get_summary_invalid_game_id(client: TestClient):
    """
    Test generating a game summary for a non-existent game.

    This should return a 404 error since the game ID does not exist.
    """
    # Act
    response = client.get(f"/games/99999/summary")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"
