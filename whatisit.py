from transformers import pipeline

pipe = pipeline("audio-classification", model="MIT/ast-finetuned-audioset-10-10-0.4593")
result = pipe("your_noise.mp3")
print(result)
