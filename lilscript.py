import torch
import numpy as np
import os
from tqdm import tqdm
from transformers import AutoProcessor, MusicGenForConditionalGeneration
from scipy.io.wavfile import write as write_wav

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
MAX_TOKENS_PER_CHUNK = 256  # controls chunk size

# -------------------------------
# Initialize model and processor
# -------------------------------
print("[INFO] Loading MusicGen-small model and processor...")
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicGenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
print(f"[INFO] Model loaded on {device}")

# -------------------------------
# Generate in chunks
# -------------------------------
num_chunks = TOTAL_DURATION // CHUNK_DURATION
all_audio = []

print(f"[INFO] Starting generation: {TOTAL_DURATION}s total, {CHUNK_DURATION}s per chunk ({num_chunks} chunks)")

for i in tqdm(range(num_chunks), desc="Generating chunks"):
    print(f"\n[INFO] Generating chunk {i+1}/{num_chunks}...")
    
    # Prepare input
    inputs = processor(
        text=[TEXT_PROMPT],
        padding=True,
        return_tensors="pt"
    ).to(device)
    
    # Generate audio
    with torch.no_grad():
        audio_values = model.generate(**inputs, max_new_tokens=MAX_TOKENS_PER_CHUNK)
    
    # Convert to numpy array
    audio_array = audio_values[0, 0].cpu().numpy()
    all_audio.append(audio_array)
    
    # Save intermediate chunk
    chunk_file = os.path.join(OUTPUT_DIR, f"chunk_{i+1}.wav")
    sampling_rate = model.config.audio_encoder.sampling_rate
    write_wav(chunk_file, rate=sampling_rate, data=audio_array)
    print(f"[INFO] Chunk {i+1} saved to {chunk_file}, length: {audio_array.shape[0]/sampling_rate:.2f}s")

# -------------------------------
# Concatenate all chunks
# -------------------------------
print("[INFO] Concatenating all chunks...")
final_audio = np.concatenate(all_audio)
final_file = "power_ballad_full.wav"
write_wav(final_file, rate=sampling_rate, data=final_audio)
print(f"[DONE] Full power ballad saved to {final_file}")
