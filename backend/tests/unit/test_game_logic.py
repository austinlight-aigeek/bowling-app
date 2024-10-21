import pytest
from app.db.models import Game, Frame

# Docstring for the module
"""
This module contains unit tests for edge cases in the bowling game logic, 
including perfect games, spares, strikes, gutter games, and invalid inputs.
"""


def test_perfect_game(db_session):
    """
    Test that a perfect game (12 consecutive strikes) results in a score of 300.
    """
    game = Game(player="Perfect Player")
    db_session.add(game)
    db_session.commit()

    # Simulate a perfect game
    for i in range(12):  # 12 strikes in a perfect game
        frame = Frame(game_id=game.id, frame_number=i + 1, rolls=[10])
        db_session.add(frame)

    db_session.commit()

    # Verify that the total score is 300
    total_score = game.calculate_score()
    assert total_score == 300


def test_gutter_game(db_session):
    """
    Test that a gutter game (0 pins every roll) results in a score of 0.
    """
    game = Game(player="Gutter Player")
    db_session.add(game)
    db_session.commit()

    # Simulate a gutter game (0 pins every roll)
    for i in range(10):  # 10 frames in a game
        frame = Frame(game_id=game.id, frame_number=i + 1, rolls=[0, 0])
        db_session.add(frame)

    db_session.commit()

    # Verify that the total score is 0
    total_score = game.calculate_score()
    assert total_score == 0


def test_spare_calculation(db_session):
    """
    Test that a spare adds the score of the next roll to the current frame.
    """
    game = Game(player="Spare Player")
    db_session.add(game)
    db_session.commit()

    # Simulate a spare in the first frame (e.g., 5 + 5) and a regular roll in the next frame (e.g., 3)
    frame1 = Frame(game_id=game.id, frame_number=1, rolls=[5, 5])  # Spare
    frame2 = Frame(game_id=game.id, frame_number=2, rolls=[3, 2])
    db_session.add(frame1)
    db_session.add(frame2)

    db_session.commit()

    # Verify that the score for the spare frame is 13 (5 + 5 + 3)
    total_score = game.calculate_score()
    assert total_score == 18  # 13 for the first frame + 5 for the second frame


def test_strike_calculation(db_session):
    """
    Test that a strike adds the score of the next two rolls to the current frame.
    """
    game = Game(player="Strike Player")
    db_session.add(game)
    db_session.commit()

    # Simulate a strike in the first frame and a regular frame afterward
    frame1 = Frame(game_id=game.id, frame_number=1, rolls=[10])  # Strike
    frame2 = Frame(game_id=game.id, frame_number=2, rolls=[4, 3])
    db_session.add(frame1)
    db_session.add(frame2)

    db_session.commit()

    # Verify that the score for the strike frame is 17 (10 + 4 + 3)
    total_score = game.calculate_score()
    assert total_score == 24  # 17 for the first frame + 7 for the second frame


def test_tenth_frame_bonus(db_session):
    """
    Test that in the 10th frame, the player can roll three times if they score a strike or spare.
    """
    game = Game(player="Bonus Player")
    db_session.add(game)
    db_session.commit()

    # Simulate a 10th frame with a strike, followed by two bonus rolls
    for i in range(9):
        frame = Frame(game_id=game.id, frame_number=i + 1, rolls=[10])
        db_session.add(frame)

    # In the 10th frame, the player gets a strike and two bonus rolls
    frame10 = Frame(
        game_id=game.id, frame_number=10, rolls=[10, 10, 10]
    )  # Three strikes
    db_session.add(frame10)

    db_session.commit()

    # Verify that the total score is 300
    total_score = game.calculate_score()
    assert total_score == 300


def test_invalid_rolls(db_session):
    """
    Test handling of invalid rolls (e.g., negative values or too many pins in a frame).
    """
    game = Game(player="Invalid Player")
    db_session.add(game)
    db_session.commit()

    # Simulate invalid rolls: Negative pins and too many pins in a single roll
    with pytest.raises(ValueError):
        frame = Frame(game_id=game.id, frame_number=1, rolls=[-1, 5])  # Negative value

    with pytest.raises(ValueError):
        frame = Frame(
            game_id=game.id, frame_number=1, rolls=[6, 6]
        )  # Too many pins in one frame
