import os
import requests

def generate_image_request(prompt: str):
    # 1. Base configuration
    # Replace with your actual endpoint URL
    url = "https://example.com"  
    
    # Safely retrieve your API key from environment variables
    api_key = os.getenv("API_KEY_VARIABLE_NAME", "YOUR_FALLBACK_API_KEY")

    # 2. Add realistic browser headers to bypass CloudFront blocks
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 3. Request payload
    payload = {
        "prompt": prompt
    }

    print(f"Generating image for prompt: {prompt}")

    try:
        # 4. Execute POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # This will raise an error if the status code is 4xx or 5xx
        response.raise_for_status()
        
        # Successful response processing
        data = response.json()
        print("Image generation successful!")
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"\n--- HTTP Error Occurred ({response.status_code}) ---")
        # Check if CloudFront returned an HTML error instead of JSON
        if "text/html" in response.headers.get("Content-Type", ""):
            print("CloudFront blocked the request before reaching the API.")
            print("Common causes: Blocked IP, missing User-Agent, or strict WAF rules.")
        else:
            print(f"API Error Details: {response.text}")
            
    except requests.exceptions.RequestException as err:
        print(f"\n--- Network or Connection Error ---")
        print(err)
        
    except ValueError:
        print("\n--- Parsing Error ---")
        print("Could not parse JSON response. Received raw text:")
        print(response.text)

    return None

# Example usage:
if __name__ == "__main__":
    test_prompt = "A futuristic cybernetic owl perched on a branch"
    generate_image_request(test_prompt)
