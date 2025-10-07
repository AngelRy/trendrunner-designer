import os
from dotenv import load_dotenv
from openai import OpenAI
import subprocess

# ✅ Load .env file automatically
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# ✅ Read API key from environment
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ Missing OPENAI_API_KEY. Please set it in your .env file.")

# ✅ Initialize client with key
client = OpenAI(api_key=api_key)

def generate_slogan(keyword, n=3):
    """
    Generate n short, catchy slogans for the given keyword.
    Uses OpenAI first, then falls back to local Ollama if needed.
    """

    base_prompt = f"""
    You are a creative slogan generator for a running clothing brand.

    TASK:
    Create {n} short, catchy, and inspiring slogans (max 6 words each)
    based on the theme: "{keyword}".

    RULES:
    - Avoid metaphors, philosophical language, and long sentences.
    - Each slogan must be distinct.
    - Output each slogan on a new line, with no numbering or punctuation.
    """

    # Try OpenAI first
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": base_prompt}],
                temperature=0.7
            )
            text = response.choices[0].message.content.strip()
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            return lines[:n]
        except Exception as e:
            print(f"⚠️ OpenAI error: {e}")
            print("Falling back to local Ollama...")

    # Fallback: local model via Ollama
    try:
        result = subprocess.run(
            ["ollama", "run", "phi3"],
            input=base_prompt,
            text=True,
            capture_output=True,
        )
        output = result.stdout.strip()

        # Basic cleanup to ensure short slogans only
        lines = [line.strip() for line in output.split("\n") if 2 <= len(line.split()) <= 6]
        if not lines:
            lines = [f"{keyword.title()} Power", f"Run {keyword.title()}", f"{keyword.title()} Energy"]
        return lines[:n]
    except Exception as e:
        print(f"⚠️ Local LLM fallback failed: {e}")
        return [f"Run {keyword.title()}", f"{keyword.title()} Spirit", f"{keyword.title()} Energy"]