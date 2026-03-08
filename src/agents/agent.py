"""
Composition Assistant Agent using Google ADK
Orchestrates the music transformation workflow using Google's Agent Development Kit

Based on: https://github.com/google/adk-python
Updated to use the current ADK API (class-based instead of decorator-based)

FIX: Added proper numpy type conversion to avoid JSON serialization errors
"""
import json
import ast
import os
import numpy as np
from typing import Any, Dict

# Import the existing utility functions
from src.utils.transcribe import transcribe_audio as do_transcribe
from src.utils.midi_json import json_to_wav, midi_to_json

# Google ADK imports - Correct API
from google.adk.agents import LlmAgent

# Configuration
from src.core.config import OLLAMA_MODEL, OLLAMA_HOST


# =============================================================================
# Helper Functions
# =============================================================================

def convert_numpy_types(obj):
    """
    Recursively convert numpy types to native Python types for JSON serialization.

    Args:
        obj: Object that may contain numpy types

    Returns:
        Object with numpy types converted to Python native types
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj


# =============================================================================
# Tool Functions for Google ADK
# Define as regular Python functions that will be passed to the Agent
# =============================================================================

def transcribe_audio_tool(audio_file_path: str) -> Dict[str, Any]:
    """Transcribe a WAV audio file into MIDI note representation.

    Uses neural network-based audio analysis (basic-pitch) to convert audio into
    a structured representation of musical notes with pitch, timing, and velocity.

    Args:
        audio_file_path: Full path to the WAV audio file to transcribe

    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - notes: Array of note objects with pitch (0-127), start (seconds),
                 end (seconds), and velocity (0-127)
        - note_count: Total number of notes extracted
        - error: Error message if status is "error"
    """
    try:
        # Use existing transcription function
        midi_obj = do_transcribe(audio_file_path)

        # Convert MIDI to JSON (this now handles numpy type conversion)
        notes_json = midi_to_json(midi_obj)

        # Ensure all values are native Python types
        notes_json = convert_numpy_types(notes_json)

        return {
            "status": "success",
            "notes": notes_json,
            "note_count": len(notes_json)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "notes": []
        }


def transform_notes_tool(notes: list, transformation_goal: str) -> Dict[str, Any]:
    """Transform MIDI notes according to music theory rules.

    Applies musical transformations using an LLM that understands music theory.
    Supports interval changes (transposition), modal shifts (scale changes),
    rhythmic alterations (timing adjustments), and register changes (octave shifts).

    Args:
        notes: Array of note objects with pitch (0-127), start (seconds),
               end (seconds), and velocity (0-127)
        transformation_goal: User's desired transformation in natural language
                           Examples: 'transpose up by 3 semitones',
                           'change to minor key', 'double the tempo',
                           'move up one octave'

    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - notes: Array of transformed note objects
        - note_count: Number of notes after transformation
        - transformation: Description of applied transformation
        - error: Error message if status is "error"
    """
    try:
        from src.clients.llm import query_llm

        # Ensure notes are native Python types before JSON serialization
        notes = convert_numpy_types(notes)

        # Convert notes to JSON string for LLM
        notes_json_str = json.dumps(notes, indent=2)

        # Query LLM with transformation goal
        llm_output = query_llm(transformation_goal, notes_json_str)

        # Parse LLM response
        try:
            edited_notes = json.loads(llm_output)
        except json.JSONDecodeError:
            try:
                # Fallback: Python-style list string
                edited_notes = ast.literal_eval(llm_output)
            except Exception:
                return {
                    "status": "error",
                    "error": f"LLM did not return valid JSON: {llm_output[:200]}...",
                    "notes": notes  # Return original notes on error
                }

        # Ensure we have a list of dicts
        if isinstance(edited_notes, dict):
            edited_notes = [edited_notes]
        elif not isinstance(edited_notes, list):
            return {
                "status": "error",
                "error": f"Expected list of dicts, got {type(edited_notes)}",
                "notes": notes
            }

        if len(edited_notes) > 0 and not isinstance(edited_notes[0], dict):
            return {
                "status": "error",
                "error": f"Expected dicts inside list, got {type(edited_notes[0])}",
                "notes": notes
            }

        # Convert numpy types in edited notes
        edited_notes = convert_numpy_types(edited_notes)

        return {
            "status": "success",
            "notes": edited_notes,
            "note_count": len(edited_notes),
            "transformation": transformation_goal
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "notes": notes
        }


def synthesize_audio_tool(notes: list, output_path: str) -> Dict[str, Any]:
    """Synthesize MIDI notes into a WAV audio file.

    Uses FluidSynth with FluidR3 General MIDI soundfont to render MIDI notes
    into high-quality audio. The output is a standard WAV file that can be
    played on any audio player.

    Args:
        notes: Array of note objects to synthesize with pitch, start, end, velocity
        output_path: Full path where the output WAV file should be saved

    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - output_path: Path to the generated WAV file
        - file_size: Size of the generated file in bytes
        - error: Error message if status is "error"
    """
    try:
        # Ensure notes are native Python types
        notes = convert_numpy_types(notes)

        # Use existing synthesis function
        json_to_wav(notes, output_path)

        # Verify file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            return {
                "status": "success",
                "output_path": output_path,
                "file_size": file_size
            }
        else:
            return {
                "status": "error",
                "error": "Output file was not created"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# =============================================================================
# Google ADK Agent Definition (Correct API)
# =============================================================================

# NOTE: Disabling Google ADK agent for now due to async event loop conflicts
# The fallback direct execution method works reliably
composition_assistant_agent = None

# Commented out until async event loop issue is resolved
# composition_assistant_agent = LlmAgent(
#     name="CompositionAssistant",
#     model="gemini-2.0-flash-exp",
#     instruction="""...""",
#     description="AI-powered music transformation and composition assistant",
#     tools=[transcribe_audio_tool, transform_notes_tool, synthesize_audio_tool],
# )


# =============================================================================
# Main Agent Function (API Entry Point)
# =============================================================================

def run_agent(audio_file: str, goal: str) -> None:
    """
    Main agent function to orchestrate the music transformation workflow.

    Currently uses direct tool execution due to asyncio event loop conflicts
    with FastAPI. The Google ADK agent integration is disabled until this is resolved.

    Args:
        audio_file: Path to the input WAV audio file
        goal: User's transformation goal/instructions in natural language

    The workflow:
    1. Transcribe audio to MIDI notes
    2. Transform notes according to user's goal
    3. Synthesize transformed notes to audio
    """
    # Ensure output folder exists
    os.makedirs("tmp/output", exist_ok=True)

    output_path = "./tmp/output/agent_output.wav"

    print(f"🎵 Starting Composition Assistant Workflow...")
    print(f"   Input: {audio_file}")
    print(f"   Goal: {goal}")
    print(f"   Output: {output_path}")
    print()

    try:
        # Direct execution workflow
        # 1. Transcribe audio
        print("   1. Transcribing audio...")
        result = transcribe_audio_tool(audio_file)
        if result["status"] != "success":
            raise Exception(f"Transcription failed: {result.get('error')}")
        notes = result["notes"]
        print(f"   ✓ Extracted {len(notes)} notes")

        # 2. Transform notes
        print(f"   2. Transforming notes: {goal}")
        result = transform_notes_tool(notes, goal)
        if result["status"] != "success":
            raise Exception(f"Transformation failed: {result.get('error')}")
        transformed_notes = result["notes"]
        print(f"   ✓ Transformed to {len(transformed_notes)} notes")

        # 3. Synthesize audio
        print("   3. Synthesizing audio...")
        result = synthesize_audio_tool(transformed_notes, output_path)
        if result["status"] != "success":
            raise Exception(f"Synthesis failed: {result.get('error')}")
        print(f"   ✓ Generated: {output_path}")

        # Verify output was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"\n✓ Workflow complete!")
            print(f"   Output: {output_path} ({file_size:,} bytes)")
        else:
            print(f"\n⚠ Workflow completed but output file not found")

    except Exception as e:
        print(f"\n✗ Workflow failed: {str(e)}")
        print(f"   Error type: {type(e).__name__}")
        raise


# =============================================================================
# Legacy Compatibility
# =============================================================================

# The function signature remains unchanged for API compatibility
# The FastAPI endpoints can continue using run_agent(audio_file, goal) exactly as before