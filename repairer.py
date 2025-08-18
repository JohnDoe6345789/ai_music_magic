wav_file = "power_ballad_full.wav"
fixed_file = "power_ballad_fixed.wav"

with open(wav_file, "rb") as f:
    data = bytearray(f.read())

# WAV header structure:
# 'fmt ' chunk starts after 12 bytes ('RIFF' + size + 'WAVE')
# Channels field is 2 bytes at offset 22 (0-based)

data[22] = 1  # mono → low byte
data[23] = 0  # high byte

# Recalculate byte rate and block align
# ByteRate = SampleRate * NumChannels * BitsPerSample/8
# BlockAlign = NumChannels * BitsPerSample/8

# Assume sample rate = 32000, bits per sample = 16
sample_rate = int.from_bytes(data[24:28], "little")
bits_per_sample = int.from_bytes(data[34:36], "little")
num_channels = 1

byte_rate = sample_rate * num_channels * bits_per_sample // 8
block_align = num_channels * bits_per_sample // 8

data[28:32] = byte_rate.to_bytes(4, "little")
data[32:34] = block_align.to_bytes(2, "little")

# Save fixed WAV
with open(fixed_file, "wb") as f:
    f.write(data)

print(f"Fixed WAV saved: {fixed_file}")
