"""
Touch Grass - Offline Nature Identifier
Hacktoberfest 2026 Submission

Author: Sakshi Yadav
Date: October 2026

Description:
    A simple CLI tool that uses a local Ollama model (LLaVA) to identify
    plants, birds, and animals without needing an internet connection.
    Built to encourage people to go outside and explore.
"""
import ollama
client = ollama.Client(host='http://127.0.0.1:11434')
import base64
import os
import sys
from datetime import datetime

# Configuration
MODEL_NAME = "llava"
LOG_FILE = "nature_log.txt"

def encode_image_to_base64(image_path):
    """
    Reads an image file and converts it to a base64 string.
    Ollama requires base64 strings to process images locally.
    """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"[!] Error: The file '{image_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error reading image: {e}")
        sys.exit(1)

def ask_local_ai(image_base64):
    """
    Sends the image to the local Ollama model and gets an identification.
    """
    # A conversational prompt usually yields better results than a rigid list.
    prompt_text = (
        "I'm out in nature right now and I just took a photo. "
        "Can you tell me what this is? Please identify the plant, bird, or animal. "
        "Give me one cool fact about it, and let me know if I should be cautious around it. "
        "Keep it brief and friendly."
    )

    print("\n[~] Thinking locally (this might take a few seconds)...")
    
    try:
        response = client.chat(
    model=MODEL_NAME,
    messages=[{
        'role': 'user',
        'content': prompt_text,
        'images': [image_base64]
    }]
)
        return response['message']['content']
    except Exception as e:
        return f"[!] AI Error: {e}\nMake sure Ollama is running in the background (run 'ollama serve' in another terminal)."

def save_log(image_path, result):
    """Appends the result to a log file for later reference."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n--- {timestamp} ---\nImage: {image_path}\nAI: {result}\n"
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(log_entry)
        print(f"[+] Log saved to {LOG_FILE}")
    except Exception as e:
        print(f"[!] Could not save log: {e}")

def main():
    # Simple banner to make it look like a real CLI tool
    print("=" * 50)
    print("  🌿 TOUCH GRASS - OFFLINE NATURE IDENTIFIER 🌿")
    print("=" * 50)
    print("Make sure you have the 'llava' model installed (ollama pull llava)")
    print("-" * 50)

    # Get user input
    image_path = input("Enter the path to your photo (e.g., bird.jpg): ").strip()

    # Check if file exists before doing heavy lifting
    if not os.path.exists(image_path):
        print(f"\n[!] File '{image_path}' does not exist. Please check the path.")
        sys.exit(1)

    # Process the image
    print(f"[*] Loading image: {image_path}...")
    img_base64 = encode_image_to_base64(image_path)

    # Get AI result
    result = ask_local_ai(img_base64)

    # Output the result
    print("\n" + "=" * 50)
    print("  IDENTIFICATION RESULT")
    print("=" * 50)
    print(result)
    print("=" * 50)

    # Save it
    save_log(image_path, result)

if __name__ == "__main__":
    main()