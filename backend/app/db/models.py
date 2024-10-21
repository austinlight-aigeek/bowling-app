from sqlalchemy import Column, String, Integer, ForeignKey, Table, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Game(Base):
    """
    Game model to store information about a bowling game.

    Attributes:
        id (int): The primary key of the game.
        player (str): The name of the player associated with the game.
        start_time (datetime): The time the game was created.
        frames (relationship): Relationship to the Frame model.
    """

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    player = Column(String, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Establish relationship with frames
    frames = relationship("Frame", back_populates="game", cascade="all, delete-orphan")


class Frame(Base):
    """
    Frame model to store details of a frame in a bowling game.

    Attributes:
        id (int): The primary key of the frame.
        game_id (int): Foreign key linking to the Game table.
        frame_number (int): The frame number (1 to 10).
        rolls (ARRAY of int): The rolls in this frame (1-3 rolls for the 10th frame).
    """

    __tablename__ = "frames"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(
        Integer, ForeignKey("games.id"), nullable=False
    )  # Link to the games table
    frame_number = Column(Integer, nullable=False)  # 1 to 10
    rolls = Column(
        ARRAY(Integer), nullable=False
    )  # Array of rolls for that frame (can be 1 to 3 rolls)

    # Establish relationship with the Game model
    game = relationship("Game", back_populates="frames")
