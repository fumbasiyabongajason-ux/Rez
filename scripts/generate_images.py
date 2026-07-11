import os
import requests

def generate_flux_image(prompt: str):
    # 1. Target the official Black Forest Labs global endpoint
    url = "https://bfl.ai"  # Change to flux-1-dev or flux-1-pro if needed
    
    # 2. Retrieve your BFL API key from your wired secrets
    api_key = os.getenv("BFL_API_KEY") 
    
    if not api_key:
        print("Error: 'BFL_API_KEY' environment secret is empty or missing.")
        return None

    # 3. Explicitly construct headers including the strict content-type and X-Key format
    headers = {
        # Using a verified, modern Chrome User-Agent to bypass CloudFront bot filters
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # 4. Set the JSON payload parameters for FLUX requirements
    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 768,
        "accept": "image/jpeg"
    }

    print(f"Generating FLUX image for prompt: {prompt}")

    try:
        # Execute POST request to BFL
        response = requests.post(url, json=payload, headers=headers)
        
        # Capture a WAF / CloudFront blocking event early
        if response.status_code == 403:
            print("\n--- CloudFront 403 Block Triggered ---")
            if "text/html" in response.headers.get("Content-Type", ""):
                print("CloudFront dropped this request. Check if 'BFL_API_KEY' is active and valid.")
                print("If running via CI/CD (like GitHub Actions), CloudFront may be dropping the runner IP.")
            else:
                print(f"BFL Refusal Details: {response.text}")
            return None

        response.raise_for_status()
        
        # BFL endpoints return a task ID to poll for the image link
        result = response.json()
        print("Request registered successfully!")
        print(f"Task Details: {result}")
        return result

    except requests.exceptions.RequestException as err:
        print(f"\n--- Transport/Network Error ---")
        print(err)
        return None

if __name__ == "__main__":
    test_prompt = "A futuristic cybernetic owl perched on a branch"
    generate_flux_image(test_prompt)
