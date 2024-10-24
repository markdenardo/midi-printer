import numpy as np
import pyaudio
import mido
import time

# Constants
SAMPLE_RATE = 44100  # Samples per second
AMPLITUDE = 0.5      # Volume
CHANNELS = 32        # Number of MIDI channels
WAVEFORMS = ['sine', 'saw', 'triangle']

# Initialize audio output
audio = pyaudio.PyAudio()

# Helper functions to generate different waveforms
def generate_sine_wave(frequency, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return AMPLITUDE * np.sin(2 * np.pi * frequency * t)

def generate_saw_wave(frequency, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return AMPLITUDE * 2 * (t * frequency - np.floor(0.5 + t * frequency))

def generate_triangle_wave(frequency, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return AMPLITUDE * (2 * np.abs(2 * (t * frequency - np.floor(0.5 + t * frequency))) - 1)

# Map MIDI channel to waveform
def get_waveform(channel):
    index = (channel - 1) % len(WAVEFORMS)
    return WAVEFORMS[index]

# Generate waveform for a note
def generate_waveform(note, duration, waveform_type):
    frequency = 440.0 * (2.0 ** ((note - 69) / 12.0))  # MIDI note to frequency
    if waveform_type == 'sine':
        return generate_sine_wave(frequency, duration)
    elif waveform_type == 'saw':
        return generate_saw_wave(frequency, duration)
    elif waveform_type == 'triangle':
        return generate_triangle_wave(frequency, duration)
    else:
        return np.zeros(int(SAMPLE_RATE * duration))  # Silence if unknown waveform

# Play waveform using PyAudio
def play_waveform(waveform):
    stream = audio.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, output=True)
    stream.write(waveform.astype(np.float32).tobytes())
    stream.close()

# MIDI event handler
def handle_midi_event(msg):
    if msg.type == 'note_on' and msg.velocity > 0:
        channel = msg.channel + 1
        note = msg.note
        duration = 0.5  # Fixed duration for simplicity
        waveform_type = get_waveform(channel)
        waveform = generate_waveform(note, duration, waveform_type)
        play_waveform(waveform)
    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
        # You can handle note off events here if needed
        pass

# Main function
def main():
    print("Starting 32-channel MIDI player...")
    with mido.open_input() as midi_input:
        while True:
            for msg in midi_input.iter_pending():
                handle_midi_event(msg)
            time.sleep(0.01)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        audio.terminate()