import os
import torch
import numpy as np
from tqdm import tqdm
from scipy.io.wavfile import write as write_wav
from audiocraft.models import MusicGen

# -------------------------------
# Settings
# -------------------------------
OUTPUT_DIR = "generated_chunks"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHUNK_DURATION = 10  # seconds per chunk
TOTAL_DURATION = 40  # total song length in seconds
TEXT_PROMPT = """
Epic female-fronted power ballad, soaring chorus, emotional verses,
soft intros building to thunderous climax, speaker-shattering intensity
"""

# -------------------------------
# Initialize model
# -------------------------------
print("[INFO] Loading MusicGen-small model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = MusicGen.get_pretrained('small', device=device)
model.set_generation_params(duration=CHUNK_DURATION)
sampling_rate = model.sample_rate
print(f"[INFO] Model loaded on {device}, sampling rate: {sampling_rate}")

# -------------------------------
# Generate in chunks
# -------------------------------
num_chunks = TOTAL_DURATION // CHUNK_DURATION
all_audio = []

print(f"[INFO] Starting generation: {TOTAL_DURATION}s total, {CHUNK_DURATION}s per chunk ({num_chunks} chunks)")

for i in tqdm(range(num_chunks), desc="Generating chunks"):
    tqdm.write(f"[INFO] Generating chunk {i+1}/{num_chunks}...")
    
    # Generate chunk
    audio_array = model.generate(TEXT_PROMPT)
    
    # Convert float32 [-1,1] to int16 for WAV saving
    audio_int16 = (audio_array * 32767).astype(np.int16)
    all_audio.append(audio_int16)
    
    # Save intermediate chunk
    chunk_file = os.path.join(OUTPUT_DIR, f"chunk_{i+1}.wav")
    write_wav(chunk_file, rate=sampling_rate, data=audio_int16)
    tqdm.write(f"[INFO] Chunk {i+1} saved to {chunk_file}, length: {audio_array.shape[0]/sampling_rate:.2f}s")

# -------------------------------
# Concatenate all chunks
# -------------------------------
print("[INFO] Concatenating all chunks...")
final_audio = np.concatenate(all_audio, axis=0)
final_file = "power_ballad_full.wav"
write_wav(final_file, rate=sampling_rate, data=final_audio)
print(f"[DONE] Full power ballad saved to {final_file}")
