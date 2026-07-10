import os
import sys
import requests

# 1. Base configuration
API_URL = "https://huggingface.co"
token = os.getenv("HF_API_TOKEN")

if not token:
    print("Error: HF_API_TOKEN environment variable is missing.")
    sys.exit(1)

headers = {"Authorization": f"Bearer {token}"}

# 2. Get inputs from GitHub Action environment
prompt = os.getenv("IMAGE_PROMPT", "A futuristic cybernetic owl perched on a branch")
filename = os.getenv("OUTPUT_FILENAME", "flux-output")

print(f"Generating image for prompt: {prompt}")

# 3. Request generation from Hugging Face Inference API
response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

if response.status_code == 200:
    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)
    
    # Save the binary image payload
    output_path = f"output/{filename}.png"
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Success! Image saved to {output_path}")
else:
    print(f"API Error ({response.status_code}): {response.text}")
    sys.exit(1)
