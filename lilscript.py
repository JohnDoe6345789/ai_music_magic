import os
import torch
import numpy as np
from scipy.io.wavfile import write as write_wav
from pydub import AudioSegment
from audiocraft.models import MusicGen

# -------------------------------
# Settings
# -------------------------------
OUTPUT_DIR = "generated_chunks"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHUNK_DURATION = 1   # seconds per chunk
TOTAL_DURATION = 40  # total song length in seconds
TEXT_PROMPT = """
Epic female-fronted power ballad, soaring chorus, emotional verses,
soft intros building to thunderous climax, speaker-shattering intensity
"""

FINAL_WAV = "power_ballad_fixed.wav"
FINAL_MP3 = "power_ballad_fixed.mp3"

# -------------------------------
# Initialize model
# -------------------------------
device = "cpu"
print("[INFO] Loading MusicGen-small on CPU...")
model = MusicGen.get_pretrained('facebook/musicgen-small', device=device)
model.set_generation_params(duration=CHUNK_DURATION)
sampling_rate = model.sample_rate
print(f"[INFO] Model loaded. Sampling rate: {sampling_rate} Hz")

# -------------------------------
# Generate in chunks
# -------------------------------
num_chunks = TOTAL_DURATION // CHUNK_DURATION
all_chunks = []

for i in range(num_chunks):
    print(f"[INFO] Generating chunk {i+1}/{num_chunks}...")
    
    # Generate chunk
    audio_tensor = model.generate(TEXT_PROMPT)
    
    # Convert Tensor -> NumPy int16
    audio_int16 = (audio_tensor.cpu().numpy().squeeze() * 32767).astype(np.int16)
    
    # Force mono/stereo shape
    if audio_int16.ndim == 1:
        audio_int16 = np.expand_dims(audio_int16, axis=1)
    
    # Save individual chunk
    chunk_file = os.path.join(OUTPUT_DIR, f"chunk_{i+1}.wav")
    write_wav(chunk_file, rate=sampling_rate, data=audio_int16)
    
    all_chunks.append(audio_int16)

# Concatenate all chunks
full_audio = np.concatenate(all_chunks, axis=0)

# Write final fixed WAV
write_wav(FINAL_WAV, rate=sampling_rate, data=full_audio)
print(f"[DONE] Full song saved: {FINAL_WAV}")

# -------------------------------
# Optional: Convert to MP3
# -------------------------------
try:
    audio = AudioSegment.from_wav(FINAL_WAV)
    audio.export(FINAL_MP3, format="mp3", bitrate="192k")
    print(f"[DONE] MP3 exported: {FINAL_MP3}")
except Exception as e:
    print("[WARN] MP3 conversion failed:", e)
