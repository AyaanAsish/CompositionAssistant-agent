"""
LLM Client for Composition Assistant.
Uses Ollama for music theory transformations.
"""
from ollama import Client
from src.core.config import OLLAMA_HOST, OLLAMA_MODEL

SYSTEM_PROMPT = """
You are a music-theory assistant.

Your task is to edit a MIDI piece by modifying the existing note events.
You do NOT generate completely new music from scratch.

You may perform:
- Interval changes (transpose notes up or down)
- Modal shifts (change notes to fit a new scale)
- Rhythmic alterations (adjust note start/end times)
- Register changes (move notes up/down octaves)

You may NOT:
- Discuss timbre, mixing, or production
- Reference audio files
- Output anything other than JSON

Output JSON ONLY as a list of note objects with these keys:
- "pitch": integer (0–127)
- "start": float (seconds)
- "end": float (seconds)
- "velocity": integer (0–127)

Example output:
[
  {"pitch": 60, "start": 0.0, "end": 0.5, "velocity": 100},
  {"pitch": 64, "start": 0.5, "end": 1.0, "velocity": 110}
]

Do not include explanations, text, or comments. Only output valid JSON.
"""


def query_llm(goal: str, midi_summary: str, model: str = None, host: str = None) -> str:
    """
    Query the LLM for music transformation.
    
    Args:
        goal: User's transformation goal/instructions
        midi_summary: JSON representation of MIDI notes
        model: Ollama model to use (defaults to config)
        host: Ollama host URL (defaults to config)
    
    Returns:
        LLM response with transformed JSON notes
    """
    prompt = f"""
Goal: {goal}

MIDI summary:
{midi_summary}

Return transformation actions.
"""

    # Use provided values or fall back to config
    ollama_host = host or OLLAMA_HOST
    ollama_model = model or OLLAMA_MODEL

    # Create client with configured host
    client = Client(host=ollama_host)

    response = client.chat(
        model=ollama_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    return response["message"]["content"]


def check_ollama_connection(host: str = None) -> dict:
    ollama_host = host or OLLAMA_HOST

    try:
        client = Client(host=ollama_host)
        models = client.list()

        # Robust extraction: prefer "name", fallback to "model"
        model_names = []
        for m in models.get("models", []):
            model_id = m.get("name") or m.get("model") or m.get("id")
            if model_id:
                model_names.append(model_id)

        configured_model = OLLAMA_MODEL
        model_available = (
                configured_model in model_names or
                any(configured_model in name for name in model_names)
        )

        return {
            "connected": True,
            "host": ollama_host,
            "models": model_names,
            "configured_model": configured_model,
            "model_available": model_available,
        }
    except Exception as e:
        return {
            "connected": False,
            "host": ollama_host,
            "error": str(e),
            "models": [],
            "configured_model": OLLAMA_MODEL,
            "model_available": False,
        }