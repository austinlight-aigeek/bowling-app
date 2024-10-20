from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid


# Helper function to generate unique IDs
def generate_uuid():
    return str(uuid.uuid4())


class Player(Base):
    """
    Player model representing a player participating in bowling games.

    Attributes:
        id: Auto-incremented unique identifier for the player.
        name: Name of the player.
    """

    __tablename__ = "players"

    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True
    )  # Auto-incremental ID
    name = Column(String, nullable=False)


class Game(Base):
    """
    Game model representing a bowling game.

    Attributes:
        id: Unique identifier for the game.
        current_frame: Index of the current active frame (0-9).
        player_id: Foreign key to the Player table.
    """

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    current_frame = Column(Integer, default=0)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player = relationship("Player")
    frames = relationship("Frame", back_populates="game")


class Frame(Base):
    """
    Frame model representing a frame in a bowling game.

    Attributes:
        id: Unique identifier for the frame.
        game_id: Foreign key to the Game model.
        rolls: List of Roll objects in this frame.
    """

    __tablename__ = "frames"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    game_id = Column(
        Integer, ForeignKey("games.id"), nullable=False
    )  # Ensure this is an Integer
    rolls = relationship("Roll", back_populates="frame")
    game = relationship("Game", back_populates="frames")


class Roll(Base):
    """
    Roll model representing a roll in a bowling frame.

    Attributes:
        id: Unique identifier for the roll.
        pins_knocked: Number of pins knocked down in the roll.
        frame_id: Foreign key to the Frame model.
    """

    __tablename__ = "rolls"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pins_knocked = Column(Integer, nullable=False)
    frame_id = Column(
        Integer, ForeignKey("frames.id"), nullable=False
    )  # Ensure this is an Integer
    frame = relationship("Frame", back_populates="rolls")
