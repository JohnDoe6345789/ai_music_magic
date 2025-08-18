import torch
import numpy as np
import scipy.io.wavfile as wav
import subprocess
import os

from transformers import AutoProcessor, MusicgenForConditionalGeneration

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading model...")
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)

prompt = "epic power ballad with soaring vocals and heavy drums"
wav_file = "power_ballad_fixed.wav"
repaired_file = "power_ballad_repaired.wav"
mp3_file = "power_ballad.mp3"

print("Generating audio...")
inputs = processor(text=[prompt], padding=True, return_tensors="pt").to(device)
audio_values = model.generate(**inputs, max_new_tokens=32000)

# Convert tensor → numpy int16
audio_np = audio_values[0, 0].cpu().numpy()
audio_int16 = (audio_np * 32767).astype(np.int16)

# Ensure 2D shape (mono)
if audio_int16.ndim == 1:
    audio_int16 = np.expand_dims(audio_int16, axis=1)

# Save WAV
wav.write(wav_file, 32000, audio_int16)
print(f"Raw WAV saved: {wav_file}")

# --- Repair header ---
def repair_wav_header(in_file, out_file):
    with open(in_file, "rb") as f:
        data = bytearray(f.read())

    # Force mono (1 channel)
    data[22] = 1
    data[23] = 0

    # Recalc byte rate + block align
    sample_rate = int.from_bytes(data[24:28], "little")
    bits_per_sample = int.from_bytes(data[34:36], "little")
    num_channels = 1

    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8

    data[28:32] = byte_rate.to_bytes(4, "little")
    data[32:34] = block_align.to_bytes(2, "little")

    with open(out_file, "wb") as f:
        f.write(data)

    print(f"Header repaired and saved: {out_file}")

repair_wav_header(wav_file, repaired_file)

# --- Convert to MP3 using ffmpeg ---
try:
    subprocess.run(
        ["ffmpeg", "-y", "-i", repaired_file, "-codec:a", "libmp3lame", "-b:a", "192k", mp3_file],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"MP3 saved: {mp3_file}")
except Exception as e:
    print(f"FFmpeg conversion failed: {e}")
