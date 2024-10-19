import pytest
from app.api.services.game import BowlingGame
from sqlalchemy.orm import Session
from app.db.models import Game, Player


@pytest.fixture
def sample_game(db: Session):
    """
    Fixture to create a sample game with default players.

    This fixture creates two players and a new bowling game in the database session.
    It ensures that each test has a fresh game instance to work with.

    Args:
        db (Session): SQLAlchemy database session for interacting with the database.

    Returns:
        Game: The game object with players added to it.
    """
    # Create two players for the game
    player1 = Player(name="player1")
    player2 = Player(name="player2")

    # Create a game object and assign players to it
    game = Game(players=[player1, player2])

    # Add the game and players to the database session and commit the transaction
    db.add(game)
    db.commit()

    # Return the game object for tests
    return game


def test_add_roll_open_frame(sample_game):
    """
    Test scoring an open frame (less than 10 pins in two rolls).

    This test checks that an open frame (a frame where less than 10 pins are knocked down)
    is correctly scored, and the game moves to the next frame.

    Args:
        sample_game (Game): The game instance provided by the fixture.
    """
    game = BowlingGame(sample_game)

    # First frame rolls (open frame, no strike or spare)
    game.add_roll(4)
    game.add_roll(3)

    # Check if pins knocked down are recorded properly
    assert sample_game.frames[0].rolls[0].pins_knocked == 4
    assert sample_game.frames[0].rolls[1].pins_knocked == 3

    # Verify that the score is calculated correctly (4 + 3 = 7)
    assert game.calculate_score() == 7


def test_add_roll_spare(sample_game):
    """
    Test scoring a spare (exactly 10 pins in two rolls).

    This test verifies that a spare is properly scored, meaning the next roll should
    be added to the score of the current frame where the spare was rolled.

    Args:
        sample_game (Game): The game instance provided by the fixture.
    """
    game = BowlingGame(sample_game)

    # Roll two balls for a spare
    game.add_roll(5)
    game.add_roll(5)  # Spare

    # The next roll should count towards the spare
    game.add_roll(4)

    # Verify that the score includes the spare bonus (10 + 4 = 14 for the first frame)
    assert game.calculate_score() == 18  # Frame 1: 14, Frame 2: 4


def test_add_roll_strike(sample_game):
    """
    Test scoring a strike (10 pins in one roll).

    This test ensures that a strike is scored correctly, where the next two rolls are
    added to the score of the frame in which the strike was bowled.

    Args:
        sample_game (Game): The game instance provided by the fixture.
    """
    game = BowlingGame(sample_game)

    # First roll is a strike
    game.add_roll(10)

    # Add the next two rolls that will count towards the strike's score
    game.add_roll(4)
    game.add_roll(3)

    # First frame score = 10 + 4 + 3 = 17, second frame score = 4 + 3 = 7
    assert game.calculate_score() == 24


def test_multiple_strikes(sample_game):
    """
    Test scoring multiple consecutive strikes.

    This test checks that consecutive strikes are properly scored according to the rules,
    where the strike frame's score includes the next two rolls, even if they are strikes.

    Args:
        sample_game (Game): The game instance provided by the fixture.
    """
    game = BowlingGame(sample_game)

    # First and second rolls are strikes
    game.add_roll(10)  # Strike 1
    game.add_roll(10)  # Strike 2

    # Add subsequent rolls to calculate scores for both strikes
    game.add_roll(4)
    game.add_roll(3)

    # Strike 1 score: 10 + 10 + 4 = 24
    # Strike 2 score: 10 + 4 + 3 = 17
    # Total score = 24 + 17 + 4 + 3 = 48
    assert game.calculate_score() == 48


def test_10th_frame_strike(sample_game):
    """
    Test special case for a strike in the 10th frame (extra rolls).

    This test verifies that when a strike is bowled in the 10th frame, the player
    is awarded two additional rolls to complete the game, as per bowling rules.

    Args:
        sample_game (Game): The game instance provided by the fixture.
    """
    game = BowlingGame(sample_game)

    # Simulate 9 frames of open frames (5 + 3)
    for _ in range(9):
        game.add_roll(5)
        game.add_roll(3)

    # 10th frame: strike followed by two extra rolls
    game.add_roll(10)  # Strike
    game.add_roll(7)
    game.add_roll(2)

    # First 9 frames score: 9 * (5 + 3) = 72
    # 10th frame score: 10 + 7 + 2 = 19
    # Total score = 72 + 19 = 91
    assert game.calculate_score() == 91


def test_10th_frame_spare(sample_game):
    """
    Test special case for a spare in the 10th frame (one extra roll).

    This test checks that when a spare is bowled in the 10th frame, the player
    is awarded one extra roll to complete the game, as per bowling rules.

    Args:
        sample_game (Game): The game instance provided by the fixture.
    """
    game = BowlingGame(sample_game)

    # Simulate 9 frames of open frames (5 + 3)
    for _ in range(9):
        game.add_roll(5)
        game.add_roll(3)

    # 10th frame: spare followed by one extra roll
    game.add_roll(7)
    game.add_roll(3)  # Spare
    game.add_roll(4)  # Extra roll for the spare

    # First 9 frames score: 9 * (5 + 3) = 72
    # 10th frame score: 10 + 4 = 14
    # Total score = 72 + 14 = 86
    assert game.calculate_score() == 86


def test_invalid_roll_more_than_ten_pins(sample_game):
    """
    Test that adding a roll with more than 10 pins is invalid.

    This test ensures that the game does not allow a roll where the number of pins
    knocked down exceeds 10, which is an invalid input in bowling.

    Args:
        sample_game (Game): The game instance provided by the fixture.
    """
    game = BowlingGame(sample_game)

    # Expect ValueError for an invalid roll (more than 10 pins)
    with pytest.raises(ValueError):
        game.add_roll(11)


def test_frame_advances_after_two_rolls(sample_game):
    """
    Test that the game advances to the next frame after two rolls in a regular frame.

    This test verifies that the game correctly advances to the next frame after
    two rolls in a regular frame (where less than 10 pins are knocked down).

    Args:
        sample_game (Game): The game instance provided by the fixture.
    """
    game = BowlingGame(sample_game)

    # First frame rolls
    game.add_roll(3)  # First roll
    game.add_roll(6)  # Second roll

    # The game should advance to the second frame
    assert game.current_frame == 1  # Check that the current frame is updated

    # Add a roll in the second frame and verify the frame has started
    game.add_roll(5)
    assert len(game.game.frames[1].rolls) == 1  # Check that the roll is added in the new frame
