import streamlit as st
import pandas as pd
import random
from pathlib import Path
from update_keywords import update_keywords
from image_gen import generate_design_image
from llm_utils import generate_slogan

# -----------------------------
# Load or update trending keywords
try:
    update_keywords()
except Exception as e:
    st.warning(f"⚠️ Could not update keywords online. Using local fallback. ({e})")

KEYWORDS_CSV = Path("data/sample_keywords.csv")
if not KEYWORDS_CSV.exists():
    st.error("No keyword file found. Please ensure data/sample_keywords.csv exists.")
    st.stop()

df_keywords = pd.read_csv(KEYWORDS_CSV)
if df_keywords.empty:
    st.error("The keyword file is empty. Please populate it or rerun update_keywords().")
    st.stop()

# -----------------------------
# Streamlit UI
st.set_page_config(page_title="TrendRunner Designer", layout="centered")
st.title("🏃 TrendRunner Designer")
st.markdown("Generate **trendy running T-shirt designs** with creative AI slogans!")

# Sidebar settings
st.sidebar.header("🎨 Design Settings")
num_icons = st.sidebar.slider("Number of icons per design", 1, 5, 2)
font_size = st.sidebar.slider("Font size", 20, 50, 30)
bg_color = st.sidebar.color_picker("Background color", "#ffffff")

# Generate button
if st.sidebar.button("Generate Design"):
    st.subheader("✨ Your AI-Generated Design")

    # Random keyword selection
    keyword_row = df_keywords.sample(n=1).iloc[0]
    keyword = keyword_row["keyword"]
    popularity = keyword_row["popularity_last_month"]
    st.markdown(f"**Keyword:** `{keyword}` (popularity: {popularity})")

    with st.spinner("💡 Generating slogans using AI..."):
        try:
            slogans = generate_slogan(keyword, count=3)
            slogan = random.choice(slogans).strip()
            if not slogan:
                raise ValueError("Empty slogan received")
            st.markdown(f"**Slogan:** {slogan}")
        except Exception as e:
            st.warning(f"⚠️ Could not generate slogan with LLM. Using fallback text. ({e})")
            slogan = f"Run free with {keyword.title()} spirit!"

    with st.spinner("🎨 Creating design..."):
        try:
            design_img = generate_design_image(
                slogan,
                num_icons=num_icons,
                font_size=font_size,
                bg_color=bg_color
            )
            st.image(design_img, caption="Generated T-shirt Design", width="stretch")
        except Exception as e:
            st.error(f"❌ Failed to generate design image. ({e})")

# -----------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, AI models, and creative coding.")
