import json
import ast
import os
from src.clients.llm import query_llm
from src.utils.transcribe import transcribe_audio
from src.utils.midi_json import json_to_wav, midi_to_json  # our new function

def run_agent(audio_file, goal):
    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # 1️⃣ Transcribe audio → MIDI in memory
    midi_obj = transcribe_audio(audio_file)

    # 2️⃣ Convert MIDI → JSON note events
    notes_json = midi_to_json(midi_obj)

    # 3️⃣ Send JSON + user goal/focus to LLM
    llm_output = query_llm(goal, notes_json)

    # 4️⃣ Parse LLM response (edited note events)
    try:
        edited_notes = json.loads(llm_output)  # try normal JSON first
    except json.JSONDecodeError:
        try:
            # fallback: Python-style list string
            edited_notes = ast.literal_eval(llm_output)
        except Exception:
            raise ValueError(f"LLM did not return valid JSON or list: {llm_output}")

    # Ensure we have a list of dicts
    if isinstance(edited_notes, dict):
        edited_notes = [edited_notes]
    elif not isinstance(edited_notes, list):
        raise TypeError(f"Expected a list of dicts, got {type(edited_notes)}")
    if len(edited_notes) > 0 and not isinstance(edited_notes[0], dict):
        raise TypeError(f"Expected dicts inside list, got {type(edited_notes[0])}")

    # 5️⃣ Convert edited JSON → WAV and save
    output_path = "./tmp/output/agent_output.wav"
    json_to_wav(edited_notes, output_path)

    print(f"Final playable WAV saved to {output_path}")
