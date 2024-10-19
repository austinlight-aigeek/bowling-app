from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid


# Helper function to generate unique IDs
def generate_uuid():
    return str(uuid.uuid4())


# Association table for many-to-many relationship between Player and Game
player_game_association = Table(
    'player_game',
    Base.metadata,
    Column('player_id', String, ForeignKey('players.id'), primary_key=True),
    Column('game_id', String, ForeignKey('games.id'), primary_key=True),
)


class Player(Base):
    """
    Player model representing a player participating in bowling games.

    Attributes:
        id: Unique identifier for the player.
        name: Name of the player.
    """

    __tablename__ = "players"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    games = relationship("Game", secondary=player_game_association, back_populates="players")


class Game(Base):
    """
    Game model representing a bowling game.

    Attributes:
        id: Unique identifier for the game.
        current_frame: Index of the current active frame (0-9).
        player_ids: List of player IDs participating in the game.
    """

    __tablename__ = "games"

    id = Column(String, primary_key=True, index=True)
    current_frame = Column(Integer, default=0)

    # PostgreSQL native array (for production)
    # player_ids = Column(ARRAY(String), nullable=False)

    # If using SQLite (for testing), you can store the player IDs as a comma-separated string
    player_ids = Column(String, nullable=False)

    # Method to convert player_ids from string to list (for SQLite)
    @property
    def player_ids_list(self):
        return self.player_ids.split(",") if self.player_ids else []

    @player_ids_list.setter
    def player_ids_list(self, value):
        self.player_ids = ",".join(value)


class Frame(Base):
    """
    Frame model representing a frame in a bowling game.

    Attributes:
        id: Unique identifier for the frame.
        game_id: Foreign key to the Game model.
        rolls: List of Roll objects in this frame.
    """

    __tablename__ = "frames"

    id = Column(String, primary_key=True, default=generate_uuid)
    game_id = Column(String, ForeignKey("games.id"), nullable=False)
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

    id = Column(String, primary_key=True, default=generate_uuid)
    pins_knocked = Column(Integer, nullable=False)
    frame_id = Column(String, ForeignKey("frames.id"), nullable=False)
    frame = relationship("Frame", back_populates="rolls")
