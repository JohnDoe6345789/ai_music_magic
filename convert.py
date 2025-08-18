from pydub import AudioSegment

wav_file = "power_ballad_fixed.wav"
mp3_file = "power_ballad_full.mp3"

# Load WAV
audio = AudioSegment.from_wav(wav_file)

# Export as MP3 (bitrate can be adjusted)
audio.export(mp3_file, format="mp3", bitrate="192k")

print(f"[DONE] MP3 saved as {mp3_file}")
