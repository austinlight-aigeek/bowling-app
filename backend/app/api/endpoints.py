from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.base import get_db
from app.db.models import Game, Frame
from app.api.llm import get_llm_summary
from app.db import models, schemas

router = APIRouter()


@router.post("/games", response_model=schemas.GameResponse)
def create_game(request: schemas.GameCreate, db: Session = Depends(get_db)):
    """
    Create a new game for a player.

    Args:
        request (schemas.GameCreate): The player name to associate with the game.
        db (Session): Database session dependency.

    Returns:
        dict: A dictionary containing the game ID and player name.
    """
    # Create a new game with the provided player name
    game = models.Game(player=request.player, frames=[])
    db.add(game)
    db.commit()
    db.refresh(game)

    return {"id": game.id, "player": game.player}


@router.post("/games/{game_id}/rolls")
async def record_roll(
    game_id: int, frames_update: schemas.GameFramesUpdate, db: Session = Depends(get_db)
):
    """
    Record or update rolls for a specific game.

    Args:
        game_id (int): The ID of the game to update.
        frames_update (schemas.GameFramesUpdate): Frames with updated rolls.
        db (Session): Database session dependency.

    Returns:
        str: Confirmation message if successful.
    """
    # Retrieve game from the database
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Update game frames
    for i, rolls in enumerate(frames_update.frames):
        frame = (
            db.query(models.Frame)
            .filter_by(game_id=game_id, frame_number=i + 1)
            .first()
        )
        if frame:
            frame.rolls = rolls
        else:
            frame = models.Frame(game_id=game_id, frame_number=i + 1, rolls=rolls)
            db.add(frame)
    db.commit()

    return "Rolls recorded successfully."


@router.get("/games/{game_id}/score")
def get_score(game_id: int, db: Session = Depends(get_db)):
    """
    Get the current score of a game.

    Args:
        game_id (int): The ID of the game to retrieve the score for.
        db (Session): Database session dependency.

    Returns:
        dict: The game ID and the current score.
    """
    # Retrieve game and frames from the database
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Calculate total score
    total_score = 0
    for frame in game.frames:
        total_score += sum(frame.rolls)

    return {"game_id": game_id, "score": total_score}


@router.get("/games/{game_id}/summary")
async def get_summary(game_id: int, db: Session = Depends(get_db)):
    """
    Get a natural language summary of the current game state using an LLM.

    Args:
        game_id (int): The ID of the game to retrieve the summary for.
        db (Session): Database session dependency.

    Returns:
        dict: A summary of the game.
    """
    # Retrieve game from the database
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Generate summary using an LLM
    summary = await get_llm_summary(game)

    return {"game_id": game_id, "summary": summary}
