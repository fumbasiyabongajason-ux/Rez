import os
import time
import requests

def generate_flux_hf_image():
    # 1. Pull the pipeline secrets populated by your GitHub workflow YAML
    prompt = os.getenv("IMAGE_PROMPT", "A futuristic cybernetic owl perched on a branch")
    filename = os.getenv("OUTPUT_FILENAME", "flux-output")
    hf_token = os.getenv("HF_API_TOKEN") 

    if not hf_token:
        print("Error: 'HF_API_TOKEN' environment secret is empty or missing in your repository.")
        return

    # 2. Point to the official Hugging Face inference API structure for FLUX.1-schnell
    url = "https://huggingface.co"
    
    # Hugging Face relies on standard Bearer auth mappings
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt
    }

    print(f"Submitting prompt to Hugging Face Inference API: '{prompt}'")
    
    # 3. Create the missing output target directory early
    os.makedirs("output", exist_ok=True)
    output_path = f"output/{filename}.jpg"

    try:
        # Hugging Face provides synchronous responses or initializes a cold model boot
        response = requests.post(url, json=payload, headers=headers)
        
        # If the model is loading into server memory, wait and retry automatically
        if response.status_code == 503:
            print("Model is currently loading on Hugging Face infrastructure. Sleeping 15 seconds before retry...")
            time.sleep(15)
            response = requests.post(url, json=payload, headers=headers)

        response.raise_for_status()

        # Hugging Face returns raw binary data directly for standard visual assets
        with open(output_path, 'wb') as f:
            f.write(response.content)
            
        print(f"Success! Image asset captured and saved to disk: {output_path}")
        print(f"Current local directory files: {os.listdir('output')}")

    except requests.exceptions.HTTPError as http_err:
        print(f"\n--- API Gateway Error ({response.status_code}) ---")
        print(f"Error Context Payload: {response.text}")
    except Exception as e:
        print(f"\n--- System/IO Error ---")
        print(e)

if __name__ == "__main__":
    generate_flux_hf_image()
