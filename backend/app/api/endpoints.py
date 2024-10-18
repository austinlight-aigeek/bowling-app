from fastapi import APIRouter, HTTPException
from app.models.game import Game, Roll, calculate_score
import openai
import os


router = APIRouter()

games = {}  # Store games in memory for simplicity

openai.api_key = os.getenv("OPENAI_API_KEY")


# POST /games - Create a new game
@router.post("/games")
def create_game():
    game_id = len(games) + 1
    games[game_id] = Game(id=game_id)
    return {"game_id": game_id}


# POST /games/{game_id}/rolls - Record a roll for a game
@router.post("/games/{game_id}/rolls")
def record_roll(game_id: int, roll: Roll):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    game = games[game_id]
    game.rolls.append(roll.pins)
    if len(game.rolls) >= 20:
        game.completed = True
    return {"roll": roll.pins, "game_id": game_id}


# GET /games/{game_id}/score - Get the current score
@router.get("/games/{game_id}/score")
def get_score(game_id: int):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    game = games[game_id]
    score = calculate_score(game.rolls)
    return {"game_id": game_id, "score": score}


# GET /games/{game_id}/summary - Get natural language summary
@router.get("/games/{game_id}/summary")
def get_summary(game_id: int):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    prompt = f"Summarize the bowling game with rolls: {game.rolls}"

    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=100)
    summary = response.choices[0].text.strip()

    return {"game_id": game_id, "summary": summary}
