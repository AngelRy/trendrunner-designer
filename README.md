# TrendRunner Designer

AI-powered tool to create **running-themed T-shirt designs** with slogans and graphics.  
Built with Python, Streamlit, and LLMs (OpenAI / local Ollama).

---

## Features

- Generate **trending keywords** from Google Trends (ML module)
- Create **catchy slogans** for running T-shirts using LLMs
- Generate **mockup images** with icons for designs
- Streamlit web app for **interactive design generation**

---

## Demo

![TrendRunner Demo](aux_files/T-shirt_20251007.png)
  <!-- optional screenshot -->
---

## Installation

1. Clone the repository:

```bash
git clone git@github.com:AngelRy/trendrunner-designer.git
cd trendrunner_designer
```




## Installation

1. Clone the repository:

```bash
git clone git@github.com:AngelRy/trendrunner-designer.git
cd trendrunner_designer

 
2. Create a Python virtual environment and activate it:

python -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate    # Windows (PowerShell)


3. Install dependencies:

pip install -r requirements.txt




    Create and populate your .env file:

cp .env.example .env
# Then edit .env and add your keys, e.g. OPENAI_API_KEY=sk_xxx

.env.example

Create a .env file from .env.example and put your keys there. Example .env.example contents:

# Copy to .env and fill in
OPENAI_API_KEY=YOUR_OPENAI_KEY_HERE
HF_TOKEN=YOUR_HUGGINGFACE_TOKEN_HERE

    Important: Do not commit your .env file. It contains secrets and is listed in .gitignore.

Usage

Run the Streamlit app:

streamlit run app.py

    Use the sidebar to adjust visual parameters (number of icons, font size, background color).

    Click Generate Design to produce a new slogan + mockup image.

    Use the Download button (if present) to save the PNG.

Slogan Generation Options (LLM)

The app supports multiple slogan backends; configure one or more in your .env:

    Local LLM (Ollama) — offline but resource-intensive

        Install Ollama and pull a model (see README section below)

        If available, the app will prefer the local LLM

    OpenAI API — lightweight, cloud-hosted

        Set OPENAI_API_KEY in .env

        The app will use OpenAI if a local LLM is not available or as a fallback

    Hugging Face (optional) — cloud-hosted inference via HF_TOKEN

        Set HF_TOKEN in .env if you prefer Hugging Face as a remote backend

The app will try OpenAI/local LLM in the configured order and fall back to safe template slogans if APIs/models are unavailable.
Notes for First-Time Users

    A small data/sample_keywords.csv and demo icons are included so the app can run immediately after cloning.

    If you want fully offline slogan generation, install Ollama and a compatible model; otherwise provide an OpenAI API key for cloud-based inference.

    The .gitignore excludes runtime-generated images, CSVs, and .env for safety.

    If you experience slow LLM responses locally, consider using a remote model (OpenAI or Hugging Face inference) for faster performance.

Troubleshooting

    Missing API key: ensure .env contains OPENAI_API_KEY and that you ran source venv/bin/activate before starting Streamlit.

    No icons shown: run the icon generator script to populate icons/:

python scripts/generate_icons.py

    Google Trends fetch fails: network or rate-limit issues will trigger fallback randomized keywords; the app remains usable.

License

This project is released under the MIT License. See the LICENSE file for details.
