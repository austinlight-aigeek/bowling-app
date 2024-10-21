from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.base import get_db
from app.db.models import Game
from app.api.llm import get_llm_summary
from app.db import models, schemas

router = APIRouter()


@router.post("/games", response_model=schemas.GameResponse)
def create_game(request: schemas.GameCreate, db: Session = Depends(get_db)):
    # Create a new game with the provided player name and empty rolls array
    game = models.Game(player=request.player, frames=[])
    db.add(game)
    db.commit()
    db.refresh(game)

    print(f"new game successfully created: {game.id}")

    # Return only the game ID
    return {"id": game.id, "player": game.player}


@router.post("/games/{game_id}/rolls")
async def record_roll(
    game_id: int, frames_update: schemas.GameFramesUpdate, db: Session = Depends(get_db)
):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()

    # If game doesn't exist, return an error
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Iterate through the frames to either create new frame records or update existing ones
    for index, frame_rolls in enumerate(frames_update.frames):
        frame = (
            db.query(models.Frame)
            .filter_by(game_id=game_id, frame_number=index + 1)
            .first()
        )

        if frame:
            frame.rolls = frame_rolls  # Update the rolls for the frame
        else:
            # Create a new frame if it doesn't exist
            new_frame = models.Frame(
                game_id=game_id, frame_number=index + 1, rolls=frame_rolls
            )
            db.add(new_frame)

    # Commit the changes to the database
    db.commit()

    return {"message": "frames updated successfully"}


@router.get("/games/{game_id}/score")
async def get_current_score(game_id: int, db: Session = Depends(get_db)):
    # Fetch the frames for the given game_id
    frames = db.query(models.Frame).filter(models.Frame.game_id == game_id).all()

    if not frames:
        raise HTTPException(status_code=404, detail="Game not found")

    # Calculate the score based on the retrieved frames
    score = calculate_score(frames)

    return {"game_id": game_id, "score": score}


def calculate_score(frames):
    total_score = 0
    rolls = []
    for frame in frames:
        rolls.extend(frame.rolls)  # Flatten the frames into a list of rolls

    frame_index = 0
    for frame_number in range(10):  # 10 frames in a game
        if frame_index >= len(rolls):
            break  # Prevent out-of-bounds access

        if is_strike(rolls[frame_index]):  # Strike
            # Ensure we have enough rolls to calculate the bonus for a strike
            if frame_index + 2 < len(rolls):
                total_score += 10 + rolls[frame_index + 1] + rolls[frame_index + 2]
            frame_index += 1
        elif frame_index + 1 < len(rolls) and is_spare(
            rolls[frame_index], rolls[frame_index + 1]
        ):  # Spare
            # Ensure we have enough rolls to calculate the bonus for a spare
            if frame_index + 2 < len(rolls):
                total_score += 10 + rolls[frame_index + 2]
            frame_index += 2
        else:  # Regular frame
            if frame_index + 1 < len(rolls):
                total_score += rolls[frame_index] + rolls[frame_index + 1]
            frame_index += 2

    return total_score


# Utility functions for bowling rules
def is_strike(roll):
    return roll == 10


def is_spare(roll1, roll2):
    return roll1 + roll2 == 10
