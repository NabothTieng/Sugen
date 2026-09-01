
#!/usr/bin/env python3
"""Quick, standalone check that your Gemini key + model actually work.

Does NOT touch cache/ or the pipeline.

Usage:
    python test_connection.py
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv


# Load .env from the same directory as this script
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# Read configuration from .env
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
API_KEY = os.getenv("GEMINI_API_KEY")


# Check API key
if not API_KEY:
    print("FAIL: GEMINI_API_KEY was not found.")
    print(f"       Make sure your .env file exists at:")
    print(f"       {ENV_FILE}")
    print()
    print("Your .env file should contain:")
    print("       GEMINI_API_KEY=your_api_key_here")
    print("       GEMINI_MODEL=your_model_name")
    sys.exit(1)


print(f"Using model: {MODEL_NAME}")
print(f"Key starts with: {API_KEY[:6]}... (length {len(API_KEY)})")


# Check Google GenAI package
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("\nFAIL: google-genai is not installed.")
    print("Run:")
    print("    pip install -r requirements.txt")
    sys.exit(1)


# Test Gemini connection
try:
    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents="Reply with exactly the word: OK",
        config=types.GenerateContentConfig(
            temperature=0
        ),
    )

    print("Raw response text:", repr(response.text))
    print("\nSUCCESS — your key and model both work.")
    print("You're clear to run main.py.")

except Exception as e:
    print(f"\nFAIL: {type(e).__name__}: {e}")

    print("\nCommon causes:")
    print("  - 404 NOT_FOUND: the model name is wrong/retired.")
    print("    Check GEMINI_MODEL in your .env file.")
    print("  - 400/401 API_KEY_INVALID: the API key is wrong.")
    print("  - 429 RESOURCE_EXHAUSTED: rate limit reached.")
    print("    Wait and try again.")

    sys.exit(1)
