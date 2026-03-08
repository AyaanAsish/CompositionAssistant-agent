from basic_pitch.inference import predict
import pretty_midi
import numpy as np

def transcribe_audio(audio_path: str) -> pretty_midi.PrettyMIDI:
    """
    Transcribe WAV to a PrettyMIDI object, handling
    both tuple and dict return formats from basic_pitch.predict().
    """

    result = predict(audio_path)

    # Case 1: predict returns (model_out, midi_obj, note_events)
    if isinstance(result, tuple) and len(result) >= 2:
        # second element is expected to be PrettyMIDI
        midi_candidate = result[1]
        if isinstance(midi_candidate, pretty_midi.PrettyMIDI):
            return midi_candidate

    # Case 2: some backends return a dict with raw arrays
    if isinstance(result, dict):
        # Some versions place piano roll or midi bytes under "midi" or "midi_data"
        midi_arr = None
        if "midi" in result:
            midi_arr = result["midi"]
        elif "midi_data" in result:
            midi_arr = result["midi_data"]

        if midi_arr is not None:
            pm = pretty_midi.PrettyMIDI()
            piano = pretty_midi.Instrument(program=0)

            # Turn piano‑roll into notes
            for pitch in range(midi_arr.shape[0]):
                times = np.where(midi_arr[pitch] > 0)[0]
                for t in times:
                    note = pretty_midi.Note(
                        velocity=int(midi_arr[pitch, t] * 127),
                        pitch=pitch,
                        start=t * 0.05,
                        end=(t + 1) * 0.05
                    )
                    piano.notes.append(note)

            pm.instruments.append(piano)
            return pm

    raise TypeError(
        "predict() did not return a usable MIDI format — "
        "ensure the backend (TensorFlow/ONNX/CoreML) is correctly installed"
    )
