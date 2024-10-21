from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

# Access the OPENAI_API_KEY environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_llm_summary(frames, model: str = "gpt"):
    """
    Generate a summary of the current bowling game using OpenAI's GPT-4 model.

    Args:
        frames (dict): Dictionary containing frame data.

    Returns:
        str: A generated summary of the current game status.
    """
    # Extract useful data from the frames
    game_data = extract_game_data(frames)

    # Prepare the prompt for GPT-4
    prompt = f"""
    You are a bowling expert, and you are summarizing the current bowling game status.
    
    The game consists of the following frames: {frames}.
    
    Total score: {game_data['total_score']}.
    Number of strikes: {game_data['strikes']}.
    Number of spares: {game_data['spares']}.
    Number of open frames: {game_data['open_frames']}.
    
    Please provide a clear and short summary of the game so far, highlighting key moments such as strikes, spares, and any notable trends in the game.
    """

    if model == "gpt":
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o",
        )

        # Extract and return the generated summary from the response
        return response.choices[0].message.content

    elif model == "bert":
        # Placeholder for BERT-based summarization
        return "Sorry, summarization with BERT hasn't been implemented yet."

    elif model == "t5":
        # Placeholder for T5-based summarization
        return "Sorry, summarization with T5 hasn't been implemented yet."

    elif model == "llama":
        # Placeholder for LLaMA-based summarization
        return "Sorry, summarization with LLaMA hasn't been implemented yet."

    else:
        # If the model is unknown, return an error message
        return "Sorry, the selected model is not supported."


def extract_game_data(frames):
    """
    Extracts valuable scores and statistics from the frames.

    Args:
        frames (dict): Dictionary containing frame data.

    Returns:
        dict: A dictionary containing total score, number of strikes, number of spares, and number of open frames.
    """
    total_score = 0
    strikes = 0
    spares = 0
    open_frames = 0

    for frame, rolls in frames.items():
        # Calculate score for each frame
        frame_score = sum(rolls)
        total_score += frame_score

        # Check for strike or spare
        if len(rolls) == 1 and rolls[0] == 10:
            strikes += 1
        elif len(rolls) == 2 and sum(rolls) == 10:
            spares += 1
        else:
            open_frames += 1

    return {
        "total_score": total_score,
        "strikes": strikes,
        "spares": spares,
        "open_frames": open_frames,
    }
