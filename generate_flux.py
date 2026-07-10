import os
import requests
import json

# Configuration
API_URL = "https://huggingface.co"
HEADERS = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# List your prompts here (add dozens if needed)
PROMPTS = [
    "A futuristic city in the style of cyberpunk, 8k",
    "A majestic golden retriever playing in a field of sunflowers",
    "Minimalist line art of a coffee cup on a wooden table"
]

os.makedirs("output", exist_ok=True)

for i, prompt in enumerate(PROMPTS):
    print(f"Generating image {i+1}/{len(PROMPTS)}: {prompt}")
    
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    
    if response.status_code == 200:
        with open(f"output/image_{i+1}.jpg", "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed for prompt {i+1}: {response.text}")
