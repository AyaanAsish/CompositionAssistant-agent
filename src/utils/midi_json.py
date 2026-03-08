import pretty_midi
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()  # looks for .env in current working dir or up the tree

# Now safe defaults + override from .env
DEFAULT_SOUNDFONT = os.getenv(
    "SOUNDFONT_PATH",
    "/app/FluidR3_GM/FluidR3_GM.sf2"  # fallback for Docker if .env missing
)


def midi_to_json(midi_input):
    """
    Convert a PrettyMIDI object or a MIDI file path into JSON-readable note events.
    Returns a list of dicts with keys: pitch, start, end, velocity.

    FIX: Converts numpy int64 to native Python int to avoid JSON serialization errors.
    """
    if isinstance(midi_input, pretty_midi.PrettyMIDI):
        midi = midi_input
    elif isinstance(midi_input, str):
        midi = pretty_midi.PrettyMIDI(midi_input)
    else:
        raise TypeError("midi_input must be a file path or PrettyMIDI object")

    notes_json = []
    for instrument in midi.instruments:
        for note in instrument.notes:
            notes_json.append({
                # Convert numpy types to native Python types for JSON serialization
                "pitch": int(note.pitch),  # Convert to native int
                "start": float(note.start),  # Convert to native float
                "end": float(note.end),  # Convert to native float
                "velocity": int(note.velocity)  # Convert to native int
            })

    return notes_json


def json_to_wav(
        notes_json,
        output_path,
        soundfont=DEFAULT_SOUNDFONT

):
    import os
    import numpy as np
    import pretty_midi
    from pydub import AudioSegment

    soundfont = os.path.expanduser(soundfont)
    if not os.path.isfile(soundfont):
        raise FileNotFoundError(f"SoundFont not found at {soundfont}")

    # JSON → PrettyMIDI
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    for n in notes_json:
        instrument.notes.append(
            pretty_midi.Note(
                pitch=int(n["pitch"]),
                start=float(n["start"]),
                end=float(n["end"]),
                velocity=int(n["velocity"]),
            )
        )

    midi.instruments.append(instrument)

    # Render audio (float32, range ~[-1, 1])
    audio = midi.fluidsynth(fs=44100, sf2_path=soundfont)

    # 🔒 Convert float32 → int16 (THIS IS THE FIX)
    audio = np.clip(audio, -1.0, 1.0)
    audio_int16 = (audio * 32767).astype(np.int16)

    # Create WAV
    segment = AudioSegment(
        audio_int16.tobytes(),
        frame_rate=44100,
        sample_width=2,  # int16 = 2 bytes
        channels=1,
    )

    segment.export(output_path, format="wav")