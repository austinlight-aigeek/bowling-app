import openai
from transformers import pipeline
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain import OpenAI


def get_llm_summary(frames, model: str = "gpt"):
    """
    Generate a summary for the bowling game using the specified LLM model.

    Args:
        frames (list): A list of frames with rolls for the game.
        model (str): The LLM model to use ('gpt', 'bert', 't5', 'llama').

    Returns:
        str: A natural language summary of the game.
    """

    # Initialize the LLM
    llm = OpenAI(model="gpt-4")

    # Prepare the input data for summarization
    frame_descriptions = []
    for frame_num, rolls in frames.items():
        if len(rolls) == 1:
            frame_descriptions.append(
                f"Frame {frame_num}: Strike ({rolls[0]} pins knocked down)"
            )
        elif sum(rolls) == 10:
            frame_descriptions.append(
                f"Frame {frame_num}: Spare ({rolls[0]} + {rolls[1]} pins knocked down)"
            )
        else:
            frame_descriptions.append(
                f"Frame {frame_num}: Open Frame ({rolls[0]} + {rolls[1]} pins knocked down)"
            )

    # Create a prompt for summarization
    prompt = (
        f"The bowling game consists of the following frames:\n"
        + "\n".join(frame_descriptions)
        + "\nProvide a summary of the game performance."
    )

    # Generate summary using LLM
    summary = llm(prompt)

    return summary


def _gpt_summary(prompt):
    """
    Generate a summary using GPT (OpenAI).

    Args:
        prompt (str): The prompt containing the bowling game summary instructions.

    Returns:
        str: The GPT-generated summary.
    """
    try:
        response = openai.Completion.create(
            engine="gpt-4",  # or gpt-3.5-turbo, depending on your setup
            prompt=prompt,
            max_tokens=150,  # Limit token usage
            temperature=0.7,  # Control creativity
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Failed to generate summary with GPT: {str(e)}"


def _bert_summary(prompt):
    """
    Generate a summary using BERT (Hugging Face transformers).

    Args:
        prompt (str): The prompt containing the bowling game summary instructions.

    Returns:
        str: The BERT-generated summary.
    """

    try:
        summarizer = pipeline("summarization", model="bert-base-uncased")
        summary = summarizer(prompt, max_new_tokens=100)
        return summary[0]["summary_text"]
    except Exception as e:
        return f"Failed to generate summary with BERT: {str(e)}"


def _t5_summary(prompt):
    """
    Generate a summary using T5 (Hugging Face transformers).

    Args:
        prompt (str): The prompt containing the bowling game summary instructions.

    Returns:
        str: The T5-generated summary.
    """
    try:
        summarizer = pipeline("summarization", model="t5-small")
        summary = summarizer(prompt, max_length=100, min_length=30)
        return summary[0]["summary_text"]
    except Exception as e:
        return f"Failed to generate summary with T5: {str(e)}"


def _llama_summary(prompt):
    """
    Generate a summary using LLaMA (custom model, placeholder).

    Args:
        prompt (str): The prompt containing the bowling game summary instructions.

    Returns:
        str: The LLaMA-generated summary (currently a placeholder).
    """
    # Placeholder logic for LLaMA model integration
    try:
        # If you have a local LLaMA model, you can integrate it here.
        # For now, returning a placeholder.
        return f"LLaMA summary for the following game: {prompt}"
    except Exception as e:
        return f"Failed to generate summary with LLaMA: {str(e)}"
