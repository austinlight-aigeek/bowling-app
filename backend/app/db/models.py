from sqlalchemy import Column, String, Integer, ForeignKey, Table, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    player = Column(String, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Establish relationship with frames
    frames = relationship("Frame", back_populates="game", cascade="all, delete-orphan")


class Frame(Base):
    __tablename__ = "frames"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(
        Integer, ForeignKey("games.id"), nullable=False
    )  # Link to the games table
    frame_number = Column(Integer, nullable=False)  # 1 to 10
    rolls = Column(
        ARRAY(Integer), nullable=False
    )  # Array of rolls for that frame (can be 1 to 3 rolls)

    game = relationship("Game", back_populates="frames")
