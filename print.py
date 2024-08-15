from PIL import Image
from midiutil import MIDIFile

# Load the image
image_path = '/Users/mdn/PycharmProjects/midi-printer/mlnp.png'  # Path to your PNG file
image = Image.open(image_path)
print(image_path)
# Convert to grayscale for easier processing
gray_image = image.convert('L')
width, height = gray_image.size
print("width", width, "height", height, "gray_image.size", gray_image.size)


def detect_lines(image):
    """Detects lines and their thicknesses in a grayscale image."""
    width, height = image.size
    pixels = image.load()
    line_data = []

    for y in range(height):
        line_start = None
        line_width = 0

        for x in range(width):
            if pixels[x, y] < 128:  # Threshold for detecting dark lines
                if line_start is None:
                    line_start = x
                line_width += 1
            else:
                if line_start is not None:
                    line_data.append((y, line_start, line_width))
                    line_start = None
                    line_width = 0

        if line_start is not None:
            line_data.append((y, line_start, line_width))

    return line_data


lines = detect_lines(gray_image)
print("lines", lines)

# Create a MIDI file with 4 tracks (voices)
midi = MIDIFile(4)
print("midi", midi)

# Set track properties
for track in range(4):
    midi.addTrackName(track, time=0, trackName=f"Voice {track + 1}")
    midi.addTempo(track, time=0, tempo=120)

print("track", track)


def map_lines_to_midi(midi, lines):
    """Maps detected lines to MIDI notes."""
    for (y, start_x, width) in lines:
        # Map line width to channel (voice)
        channel = min(width // 5, 3)  # Scale to 4 channels

        # Map y-position to pitch
        pitch = 60 + (y // 10)  # Example pitch mapping

        # Add note to the corresponding track
        midi.addNote(
            track=channel,
            channel=channel,
            pitch=pitch,
            time=start_x / 100,  # Map start_x to time (arbitrary scale)
            duration=1,  # Fixed duration for simplicity
            volume=100
        )


map_lines_to_midi(midi, lines)

# Save the MIDI file
output_midi_path = 'output.mid'
with open(output_midi_path, 'wb') as output_file:
    midi.writeFile(output_file)

print("MIDI file created successfully!")
