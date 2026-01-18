import librosa
import pretty_midi


def load_audio(filepath):
    """
    Loads an audio file without resampling.

    Returns:
        y (np.ndarray): audio waveform
        sr (int): sample rate
        duration (float): seconds
    """
    y, sr = librosa.load(filepath, sr=None)
    duration = len(y) / sr
    return y, sr, duration


def load_midi(filepath):
    midi = pretty_midi.PrettyMIDI(filepath)
    instrument = midi.instruments[0]

    notes = []
    for note in instrument.notes:
        notes.append({
            "pitch": note.pitch,
            "start": note.start,
            "end": note.end,
            "velocity": note.velocity
        })

    return notes


def save_midi(notes, output_path):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    for n in notes:
        instrument.notes.append(
            pretty_midi.Note(
                pitch=n["pitch"],
                start=n["start"],
                end=n["end"],
                velocity=n["velocity"]
            )
        )

    midi.instruments.append(instrument)
    midi.write(output_path)