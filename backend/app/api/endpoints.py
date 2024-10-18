from fastapi import APIRouter, HTTPException
from app.models.game import Game, Roll, calculate_score
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
games = {}  # Store games in memory for simplicity


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


@router.get("/games/{game_id}/summary")
def get_summary(game_id: int, model: str = "gpt"):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    rolls_summary = f"Summarize the bowling game with rolls: {game.rolls}"

    # Depending on the model parameter, use either GPT or BERT
    if model.lower() == "gpt":
        return get_gpt_summary(game_id, game)
    elif model.lower() == "bert":
        return get_bert_summary(game_id, game)
    else:
        raise HTTPException(
            status_code=400, detail="Invalid model type. Choose 'gpt' or 'bert'."
        )


def get_gpt_summary(game_id: int, game: Game):
    try:
        # Initialize OpenAI client with the API key
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Craft a detailed prompt to help GPT generate better summaries
        prompt = (
            f"You're summarizing a bowling game. The game ID is {game_id}. "
            f"The rolls in the game are: {game.rolls}. "
            f"Provide a detailed but concise description of the game progress, key moments, and current score. "
            f"Highlight important rolls like strikes and spares, and mention if the game is nearing completion."
        )

        # Call the chat completion API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4",  # Or "gpt-3.5-turbo"
        )

        # Extract and return the generated summary using dot notation
        summary = chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")  # Log detailed error message
        raise HTTPException(
            status_code=500, detail=f"Error generating GPT summary: {e}"
        )

    return {"summary": summary}


def get_bert_summary(game_id: int, game: Game):
    # Add prompt engineering to structure the input for BERT
    structured_prompt = (
        f"BOWLING GAME ID {game_id}. Rolls: {game.rolls}. "
        f"Key events: Any strikes? Any spares? What's the score? "
        f"Summarize the game progress and focus on important rolls."
    )

    from transformers import pipeline

    summarizer = pipeline("summarization", model="t5-small")

    # Setting max_new_tokens to limit the additional generated tokens and prevent length issues
    summary = summarizer(
        structured_prompt,
        max_length=100,  # Increase max_length or adjust according to input
        min_length=25,
        max_new_tokens=50,  # Set max new tokens to avoid exceeding input length limits
        do_sample=False,
    )

    return {"summary": summary[0]["summary_text"]}
