from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import openai
import os

app = FastAPI()

# In-memory store for games (for simplicity, use a database in production)
games = {}

# Load environment variables for OpenAI key (set this in your .env file)
openai.api_key = os.getenv("OPENAI_API_KEY")


# Models
class Roll(BaseModel):
    pins: int


class Game(BaseModel):
    id: int
    rolls: List[int] = []
    current_frame: int = 1
    completed: bool = False


# API Endpoints


@app.post("/games", response_model=Game)
def create_game():
    game_id = len(games) + 1
    new_game = Game(id=game_id)
    games[game_id] = new_game
    return new_game


@app.post("/games/{game_id}/rolls", response_model=Game)
def record_roll(game_id: int, roll: Roll):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    if game.completed:
        raise HTTPException(status_code=400, detail="Game is already completed")

    # Append the roll and handle the game state (this is simplified)
    game.rolls.append(roll.pins)

    if len(game.rolls) >= 20 or (len(game.rolls) == 10 and all(p == 10 for p in game.rolls[:10])):
        game.completed = True

    return game


@app.get("/games/{game_id}/score")
def get_score(game_id: int):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    return calculate_score(game.rolls)


@app.get("/games/{game_id}/summary")
def get_game_summary(game_id: int):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]

    # Convert game data into a prompt for LLM
    summary_prompt = f"Summarize the bowling game: rolls: {game.rolls}"

    try:
        response = openai.Completion.create(engine="text-davinci-003", prompt=summary_prompt, max_tokens=50)
        summary = response.choices[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating summary")

    return {"summary": summary}


# Function to calculate score based on rolls (simplified version of bowling scoring rules)
def calculate_score(rolls: List[int]) -> int:
    score = 0
    roll_index = 0
    for frame in range(10):
        if rolls[roll_index] == 10:  # Strike
            score += 10 + rolls[roll_index + 1] + rolls[roll_index + 2]
            roll_index += 1
        elif sum(rolls[roll_index : roll_index + 2]) == 10:  # Spare
            score += 10 + rolls[roll_index + 2]
            roll_index += 2
        else:
            score += sum(rolls[roll_index : roll_index + 2])
            roll_index += 2
    return score
