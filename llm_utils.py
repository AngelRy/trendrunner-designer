# llm_utils.py
"""
Unified LLM utility for TrendRunner Designer.

Usage:
    from llm_utils import generate_slogan
    slogans = generate_slogan("trail running", count=3)
    # also accepts `n` for backwards compatibility:
    slogans = generate_slogan("trail running", n=3)
"""

import os
import subprocess
import requests
import random
from dotenv import load_dotenv

load_dotenv()

# Config from environment (with sensible defaults)
LLM_MODE = os.getenv("LLM_MODE", "huggingface")  # "online", "local", or "huggingface"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # if using OpenAI
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
LOCAL_MODEL = os.getenv("LOCAL_MODEL", "llama3.1")
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))

# Simple static fallbacks if everything else fails
STATIC_FALLBACKS = [
    "Run free",
    "Chase the trail",
    "Born to move",
    "Run with purpose",
    "Stride with pride",
]


def _clean_lines(text):
    """Split raw output into clean lines and remove bullets/numbering."""
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        # remove leading numbering or bullets like "1. " or "- " or "• "
        line = line.lstrip(" -•0123456789.").strip()
        if line:
            lines.append(line)
    return lines


def _pad_to_count(lines, count, keyword):
    """Ensure we always return exactly `count` slogans (pad if needed)."""
    res = lines[:count]
    while len(res) < count:
        # pick a semi-dynamic fallback to keep variety
        placeholder = random.choice(STATIC_FALLBACKS)
        # incorporate keyword sometimes for relevancy
        res.append(f"{placeholder} {keyword.title()}" if random.random() < 0.5 else placeholder)
    return res


def _generate_online(prompt, count):
    """Try OpenAI (if key present). Returns list of lines or raises."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "system", "content": "You are a concise slogan writer."},
                      {"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=120,
            n=1,
        )
        text = ""
        # defensive parsing
        try:
            text = response.choices[0].message.content.strip()
        except Exception:
            # try alternative shape
            text = getattr(response, "text", "").strip() or str(response)
        lines = _clean_lines(text)
        return _pad_to_count(lines, count, prompt.split("'")[1] if "'" in prompt else "")
    except Exception as e:
        raise RuntimeError(f"OpenAI generation failed: {e}")


def _generate_local(prompt, count):
    """Try local Ollama (if installed). Returns list of lines or raises."""
    try:
        cmd = ["ollama", "run", LOCAL_MODEL]
        # Pass prompt via stdin for safety
        proc = subprocess.run(
            cmd,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=LLM_TIMEOUT,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"ollama returned non-zero exit code: {proc.returncode} | stderr: {proc.stderr}")
        text = proc.stdout.strip()
        lines = _clean_lines(text)
        return _pad_to_count(lines, count, prompt.split("'")[1] if "'" in prompt else "")
    except Exception as e:
        raise RuntimeError(f"Local LLM failed: {e}")


def _generate_hf(prompt, count):
    """Use Hugging Face Inference API. Returns list of lines or raises."""
    if not HUGGINGFACE_API_KEY:
        raise RuntimeError("No Hugging Face API key provided.")
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 60, "temperature": 0.8}}
        url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        resp = requests.post(url, headers=headers, json=payload, timeout=LLM_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        # response shape differs by model/provider: try common places
        text = ""
        if isinstance(data, dict) and "generated_text" in data:
            text = data["generated_text"]
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            # some HF models return a list of dicts with 'generated_text'
            text = data[0].get("generated_text") or list(data[0].values())[0]
        elif isinstance(data, str):
            text = data
        else:
            # fallback to raw text
            text = str(data)
        lines = _clean_lines(text)
        return _pad_to_count(lines, count, prompt.split("'")[1] if "'" in prompt else "")
    except Exception as e:
        raise RuntimeError(f"Hugging Face generation failed: {e}")


import random

def generate_slogan(keyword, count=3, use_online=True):
    """
    Generate creative, keyword-relevant slogans.
    Prefers online LLM (OpenAI); falls back to local or template-based.
    """
    slogans = []

    prompt = f"""
    You are an expert slogan writer for running-related apparel.
    Create {count} short, catchy slogans inspired by the theme "{keyword}".
    Each slogan should:
    - Be 2–6 words long
    - Evoke motivation, strength, or endurance
    - Be clearly related to "{keyword}" (semantically), even if the word itself is not used
    - Avoid clichés and repetition
    - Sound good on a T-shirt

    Output only the slogans as a numbered list.
    """

    try:
        if use_online:
            from openai import OpenAI
            client = OpenAI()
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a creative marketing copywriter."},
                          {"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=80
            )
            text = resp.choices[0].message.content
            slogans = [line.strip("1234567890. ").strip() for line in text.splitlines() if line.strip()]
    except Exception as e:
        print(f"[Warning] Online LLM failed: {e}")

    # Fallback slogans if LLM fails
    if not slogans:
        base_fallbacks = [
            f"Run with {keyword}",
            f"Born to {keyword}",
            f"Fuel your {keyword}",
            f"Embrace the {keyword} spirit",
            f"{keyword.capitalize()} never stops"
        ]
        slogans = random.sample(base_fallbacks, k=min(count, len(base_fallbacks)))

    return slogans
