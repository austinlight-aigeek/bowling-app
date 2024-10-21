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
async def record_roll(game_id: int, frames_update: schemas.GameFramesUpdate, db: Session = Depends(get_db)):
    """
    Record or update rolls for a specific game.

    Args:
        game_id (int): The ID of the game to update.
        frames_update (schemas.GameFramesUpdate): Frames with updated rolls.
        db (Session): Database session dependency.

    Returns:
        dict: Success message.
    """
    game = db.query(models.Game).filter(models.Game.id == game_id).first()

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Iterate through the frames to either create new frame records or update existing ones
    for index, frame_rolls in enumerate(frames_update.frames):
        frame = db.query(models.Frame).filter_by(game_id=game_id, frame_number=index + 1).first()

        if frame:
            frame.rolls = frame_rolls  # Update the rolls for the frame
        else:
            new_frame = models.Frame(game_id=game_id, frame_number=index + 1, rolls=frame_rolls)
            db.add(new_frame)

    db.commit()

    return {"message": "frames updated successfully"}


@router.get("/games/{game_id}/score")
async def get_current_score(game_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the current score for a specific game.

    Args:
        game_id (int): The ID of the game.
        db (Session): Database session dependency.

    Returns:
        dict: Game ID and current score.
    """
    frames = db.query(models.Frame).filter(models.Frame.game_id == game_id).all()

    if not frames:
        raise HTTPException(status_code=404, detail="Game not found")

    score = calculate_score(frames)
    return {"game_id": game_id, "score": score}


@router.get("/players/{player_name}/statistics")
async def get_player_statistics(player_name: str, db: Session = Depends(get_db)):
    """
    Calculate and retrieve game statistics for a specific player.

    Args:
        player_name (str): The name of the player.
        db (Session): Database session dependency.

    Returns:
        dict: Player name and calculated statistics (total games, total score, highest score, lowest score, average score).
    """
    games = db.query(models.Game).filter(models.Game.player == player_name).all()

    if not games:
        raise HTTPException(status_code=404, detail="No games found for this player")

    total_games = len(games)
    total_score = 0
    highest_score = 0
    lowest_score = float("inf")

    for game in games:
        frames = db.query(models.Frame).filter(models.Frame.game_id == game.id).all()
        score = calculate_score(frames)
        total_score += score
        highest_score = max(highest_score, score)
        lowest_score = min(lowest_score, score)

    average_score = total_score / total_games if total_games > 0 else 0

    return {
        "player_name": player_name,
        "total_games": total_games,
        "total_score": total_score,
        "highest_score": highest_score,
        "lowest_score": lowest_score,
        "average_score": round(average_score, 2),
    }


@router.get("/players/{player_name}/history")
async def get_player_history(player_name: str, db: Session = Depends(get_db)):
    """
    Retrieve the historical games played by a specific player, including game scores, strikes, and spares.

    Args:
        player_name (str): The name of the player.
        db (Session): Database session dependency.

    Returns:
        dict: Player name and a list of historical games with scores, strikes, and spares.
    """
    games = db.query(models.Game).filter(models.Game.player == player_name).all()

    if not games:
        raise HTTPException(status_code=404, detail="No games found for this player")

    game_history = []

    for game in games:
        # Join the frames table with the game and calculate strikes and spares for each game
        frames = db.query(models.Frame).filter(models.Frame.game_id == game.id).all()

        score = calculate_score(frames)

        # Calculate the number of strikes and spares
        strikes = 0
        spares = 0
        for frame in frames:
            if frame.rolls[0] == 10:
                strikes += 1  # Strike
            elif len(frame.rolls) > 1 and sum(frame.rolls[:2]) == 10:
                spares += 1  # Spare

        game_history.append(
            {
                "game_id": game.id,
                "score": score,
                "strikes": strikes,
                "spares": spares,
                "start_time": game.start_time,
            }
        )

    return {"player_name": player_name, "games": game_history}


@router.get("/games/{game_id}/summary")
async def get_game_summary(game_id: int, llm: str = "gpt", db: Session = Depends(get_db)):
    """
    Fetch the summary of the current game using the selected LLM (GPT, BERT, T5, LLaMA).

    Args:
        game_id (int): The ID of the game.
        llm (str): The selected LLM for summarization (default: "gpt").
        db (Session): Database session dependency.

    Returns:
        dict: A summary of the game based on the selected LLM.
    """
    # Fetch the game by game_id
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Fetch the frames associated with the game
    frames = db.query(Frame).filter(Frame.game_id == game_id).all()

    formatted_frames = {f"Frame {i + 1}": frame.rolls for i, frame in enumerate(frames)}

    if not frames:
        raise HTTPException(status_code=404, detail="No frames found for this game")

    # Use the selected LLM to generate the summary
    if llm == "gpt":
        summary = get_llm_summary(formatted_frames, model="gpt")
    elif llm == "bert":
        summary = get_llm_summary(formatted_frames, model="bert")
    elif llm == "t5":
        summary = get_llm_summary(formatted_frames, model="t5")
    elif llm == "llama":
        summary = get_llm_summary(formatted_frames, model="llama")
    else:
        raise HTTPException(status_code=400, detail="Invalid LLM selected")

    return {"summary": summary}


def calculate_score(frames):
    """
    Calculate the total score for a game based on the frames and rolls.

    Args:
        frames (list): List of frames with rolls.

    Returns:
        int: The calculated total score for the game.
    """
    total_score = 0
    rolls = []
    for frame in frames:
        rolls.extend(frame.rolls)

    frame_index = 0
    for frame_number in range(10):  # 10 frames in a game
        if frame_index >= len(rolls):
            break

        if is_strike(rolls[frame_index]):  # Strike
            if frame_index + 2 < len(rolls):
                total_score += 10 + rolls[frame_index + 1] + rolls[frame_index + 2]
            frame_index += 1
        elif frame_index + 1 < len(rolls) and is_spare(rolls[frame_index], rolls[frame_index + 1]):  # Spare
            if frame_index + 2 < len(rolls):
                total_score += 10 + rolls[frame_index + 2]
            frame_index += 2
        else:  # Regular frame
            if frame_index + 1 < len(rolls):
                total_score += rolls[frame_index] + rolls[frame_index + 1]
            frame_index += 2

    return total_score


def is_strike(roll):
    """
    Check if a roll is a strike (10 pins knocked down).

    Args:
        roll (int): Number of pins knocked down.

    Returns:
        bool: True if the roll is a strike, False otherwise.
    """
    return roll == 10


def is_spare(roll1, roll2):
    """
    Check if two rolls are a spare (10 pins knocked down in two rolls).

    Args:
        roll1 (int): Number of pins knocked down in the first roll.
        roll2 (int): Number of pins knocked down in the second roll.

    Returns:
        bool: True if the two rolls are a spare, False otherwise.
    """
    return roll1 + roll2 == 10
