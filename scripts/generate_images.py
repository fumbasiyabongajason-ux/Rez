import os
import time
import requests

def generate_flux_image():
    prompt = os.getenv("IMAGE_PROMPT", "A futuristic cybernetic owl perched on a branch")
    filename = os.getenv("OUTPUT_FILENAME", "flux-output")
    api_key = os.getenv("BFL_API_KEY") 

    if not api_key:
        print("Error: 'BFL_API_KEY' environment secret is empty or missing.")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Step 1: Submit Task
    trigger_url = "https://bfl.ai" 
    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 768,
        "accept": "image/jpeg"
    }

    print(f"Submitting image task for prompt: '{prompt}'")
    try:
        response = requests.post(trigger_url, json=payload, headers=headers)
        response.raise_for_status()
        task_data = response.json()
        task_id = task_data.get("id")
        print(f"Task successfully registered. ID: {task_id}")
    except Exception as e:
        print(f"Failed to submit task to API: {e}")
        return

    # Step 2: High-Speed Aggressive Polling
    result_url = "https://bfl.ai"
    image_download_url = None
    
    print("\n--- Starting Aggressive Status Polling ---")
    # Checked 120 times every 0.75 seconds to ensure minimal latency overhead
    for attempt in range(1, 121):  
        time.sleep(0.75) 
        try:
            status_response = requests.get(result_url, params={"id": task_id}, headers=headers)
            status_response.raise_for_status()
            status_data = status_response.json()
            
            status = status_data.get("status")
            print(f"Check {attempt} | Status: {status}")

            if status == "Ready":
                image_download_url = status_data.get("result", {}).get("sample")
                print("Image generation complete!")
                break
            elif status in ["Failed", "Error"]:
                print(f"BFL backend stopped with error status: {status}")
                return
        except Exception as e:
            print(f"Polling connection issue: {e}")
            return
            
    if not image_download_url:
        print("Timeout reached: Image generation took too long or status never became 'Ready'.")
        return

    # Step 3: Download Asset
    os.makedirs("output", exist_ok=True)
    output_path = f"output/{filename}.jpg"

    print(f"Downloading image from asset repository: {image_download_url}")
    try:
        img_response = requests.get(image_download_url, stream=True)
        img_response.raise_for_status()
        with open(output_path, 'wb') as file:
            for chunk in img_response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Success! Saved image to local folder: {output_path}")
    except Exception as e:
        print(f"Failed to save image payload to disk: {e}")

if __name__ == "__main__":
    generate_flux_image()
