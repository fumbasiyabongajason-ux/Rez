import os
import time
import requests

def generate_flux_image():
    # 1. Gather variables from the GitHub Action environment parameters
    prompt = os.getenv("IMAGE_PROMPT", "A futuristic cybernetic owl perched on a branch")
    filename = os.getenv("OUTPUT_FILENAME", "flux-output")
    api_key = os.getenv("BFL_API_KEY") 

    if not api_key:
        print("Error: 'BFL_API_KEY' environment secret is empty or missing.")
        return

    # 2. Establish strict headers required for official BFL API routing
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # 3. Step 1: Submit the Text-to-Image Generation Task
    trigger_url = "https://bfl.ai" # Or flux-1-dev based on budget
    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 768,
        "accept": "image/jpeg"
    }

    print(f"Submitting image task to BFL for prompt: '{prompt}'")
    try:
        response = requests.post(trigger_url, json=payload, headers=headers)
        response.raise_for_status()
        task_data = response.json()
        task_id = task_data.get("id")
        print(f"Task successfully registered. ID: {task_id}")
    except Exception as e:
        print(f"Failed to submit task to API: {e}")
        if 'response' in locals():
            print(f"Response content: {response.text}")
        return

    # 4. Step 2: Poll the task endpoint until the generation is complete
    result_url = "https://bfl.ai"
    image_download_url = None
    
    print("Waiting for image to generate (polling API)...")
    for attempt in range(30):  # Poll for up to 2.5 minutes
        time.sleep(5)
        try:
            status_response = requests.get(result_url, params={"id": task_id}, headers=headers)
            status_response.raise_for_status()
            status_data = status_response.json()
            status = status_data.get("status")

            if status == "Ready":
                image_download_url = status_data.get("result", {}).get("sample")
                print("Image generation complete!")
                break
            elif status == "Failed":
                print("BFL backend reported generation failure.")
                return
            else:
                print(f"Status is still '{status}'... checking again in 5 seconds.")
        except Exception as e:
            print(f"Polling check error: {e}")
            return
            
    if not image_download_url:
        print("Timeout reached: Image took too long to generate.")
        return

    # 5. Step 3: Download the file and write to the output folder
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
        print(f"Directory listing for verification: {os.listdir('output')}")
    except Exception as e:
        print(f"Failed to save image payload to disk: {e}")

if __name__ == "__main__":
    generate_flux_image()
