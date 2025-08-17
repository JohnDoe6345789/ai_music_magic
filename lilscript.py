import os
import torch
import numpy as np
from time import time
from scipy.io.wavfile import write as write_wav
from audiocraft.models import MusicGen

# -------------------------------
# Settings
# -------------------------------
OUTPUT_DIR = "generated_chunks"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHUNK_DURATION = 5   # seconds per chunk (CPU-friendly)
TOTAL_DURATION = 40  # total song length in seconds
TEXT_PROMPT = """
Epic female-fronted power ballad, soaring chorus, emotional verses,
soft intros building to thunderous climax, speaker-shattering intensity
"""

# Force CPU usage
device = "cpu"
print(f"[INFO] Loading MusicGen-small model on CPU...")

# -------------------------------
# Initialize model
# -------------------------------
model = MusicGen.get_pretrained('small', device=device)
model.set_generation_params(duration=CHUNK_DURATION)
sampling_rate = model.sample_rate
print(f"[INFO] Model loaded on CPU, sampling rate: {sampling_rate}")

# -------------------------------
# Generate in chunks
# -------------------------------
num_chunks = TOTAL_DURATION // CHUNK_DURATION
final_file = "power_ballad_full.wav"

print(f"[INFO] Starting generation: {TOTAL_DURATION}s total, {CHUNK_DURATION}s per chunk ({num_chunks} chunks)")

for i in range(num_chunks):
    start_time = time()
    print(f"[INFO] Generating chunk {i+1}/{num_chunks}...")

    # Generate chunk (CPU may take ~60s per 5s chunk)
    audio_array = model.generate(TEXT_PROMPT)

    # Convert float32 [-1,1] to int16 immediately to save RAM
    audio_int16 = (audio_array * 32767).astype(np.int16)

    # Save intermediate chunk
    chunk_file = os.path.join(OUTPUT_DIR, f"chunk_{i+1}.wav")
    write_wav(chunk_file, rate=sampling_rate, data=audio_int16)

    # Append to final WAV
    if i == 0:
        write_wav(final_file, rate=sampling_rate, data=audio_int16)
    else:
        existing = np.fromfile(final_file, dtype=np.int16)
        combined = np.concatenate([existing, audio_int16])
        write_wav(final_file, rate=sampling_rate, data=combined)

    end_time = time()
    print(f"[INFO] Chunk {i+1} done in {end_time - start_time:.1f}s, saved to {chunk_file}")

print(f"[DONE] Full power ballad saved to {final_file}")
print("[INFO] All chunks are also saved in the 'generated_chunks' folder.")
