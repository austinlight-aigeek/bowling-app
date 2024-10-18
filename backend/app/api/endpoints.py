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


@router.get("/games/{game_id}/summary")
def get_summary(game_id: int, model: str = "gpt"):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    rolls_summary = f"Summarize the bowling game with rolls: {game.rolls}"

    # Depending on the model parameter, use either GPT or BERT
    if model.lower() == "gpt":
        return get_gpt_summary(rolls_summary)
    elif model.lower() == "bert":
        return get_bert_summary(rolls_summary)
    else:
        raise HTTPException(
            status_code=400, detail="Invalid model type. Choose 'gpt' or 'bert'."
        )


def get_gpt_summary(prompt: str):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003", prompt=prompt, max_tokens=100
        )
        summary = response.choices[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating GPT summary")

    return {"summary": summary}


def get_bert_summary(prompt: str):
    # Here, you can use a BERT-based model from Hugging Face's transformers library.
    from transformers import pipeline

    summarizer = pipeline("summarization", model="bert-base-uncased")
    summary = summarizer(prompt, max_length=50, min_length=25, do_sample=False)

    return {"summary": summary[0]["summary_text"]}
