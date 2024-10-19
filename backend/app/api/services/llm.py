import openai
from transformers import pipeline


def get_llm_summary(game, model: str = "gpt"):
    """
    Generate a summary for the game using the specified LLM model.

    Args:
        game: The game object.
        model: The LLM model to use ('gpt', 'bert', 't5', 'llama').

    Returns:
        A natural language summary of the game.
    """
    if model == "gpt":
        return _gpt_summary(game)
    elif model == "bert":
        return _bert_summary(game)
    elif model == "t5":
        return _t5_summary(game)
    elif model == "llama":
        return _llama_summary(game)
    else:
        raise ValueError("Unsupported model specified")


def _gpt_summary(game):
    """
    Generate a summary using GPT (OpenAI).

    Args:
        game: The game object.

    Returns:
        GPT-generated summary.
    """
    summary_prompt = f"Summarize the bowling game with ID: {game.id}"

    response = openai.Completion.create(engine="gpt-4", prompt=summary_prompt, max_tokens=100)
    return response.choices[0].text.strip()


def _bert_summary(game):
    """
    Generate a summary using BERT (Hugging Face transformers).

    Args:
        game: The game object.

    Returns:
        BERT-generated summary.
    """
    summarizer = pipeline("summarization", model="bert-base-uncased")
    text = f"Summarize the bowling game with ID: {game.id}"
    summary = summarizer(text, max_length=100, min_length=30)
    return summary[0]['summary_text']


def _t5_summary(game):
    """
    Generate a summary using T5 (Hugging Face transformers).

    Args:
        game: The game object.

    Returns:
        T5-generated summary.
    """
    summarizer = pipeline("summarization", model="t5-small")
    text = f"Summarize the bowling game with ID: {game.id}"
    summary = summarizer(text, max_length=100, min_length=30)
    return summary[0]['summary_text']


def _llama_summary(game):
    """
    Generate a summary using LLaMA (custom model).

    Args:
        game: The game object.

    Returns:
        LLaMA-generated summary.
    """
    # Placeholder for LLaMA model integration
