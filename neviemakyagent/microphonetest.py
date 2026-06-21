from machine import ADC
import array
import time
import struct

# -----------------------------
# Settings
# -----------------------------
SAMPLE_RATE = 8000      # samples/second
RECORD_SECONDS = 5

adc = ADC(26)           # GP26 (ADC0)

num_samples = SAMPLE_RATE * RECORD_SECONDS

# Create an array to hold the samples
samples = array.array("H", [0] * num_samples)

print("Recording...")

sample_period = 1000000 // SAMPLE_RATE
next_sample = time.ticks_us()

# -----------------------------
# Record audio
# -----------------------------
for i in range(num_samples):

    samples[i] = adc.read_u16()

    next_sample = time.ticks_add(next_sample, sample_period)

    while time.ticks_diff(next_sample, time.ticks_us()) > 0:
        pass

print("Recording finished!")

# -----------------------------
# Save WAV file
# -----------------------------
with open("recording.wav", "wb") as f:

    data_size = num_samples * 2

    # RIFF header
    f.write(b"RIFF")
    f.write(struct.pack("<I", data_size + 36))
    f.write(b"WAVE")

    # fmt chunk
    f.write(b"fmt ")
    f.write(struct.pack(
        "<IHHIIHH",
        16,                 # chunk size
        1,                  # PCM
        1,                  # mono
        SAMPLE_RATE,
        SAMPLE_RATE * 2,
        2,
        16
    ))

    # data chunk
    f.write(b"data")
    f.write(struct.pack("<I", data_size))

    # Write samples
    for sample in samples:
        f.write(struct.pack("<H", sample))

print("Saved recording.wav")
