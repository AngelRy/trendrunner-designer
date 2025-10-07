import streamlit as st
import pandas as pd
import random
from pathlib import Path
from update_keywords import update_keywords
from image_gen import generate_design_image
from llm_utils import generate_slogan

# -----------------------------
# Update keywords (online/fallback)
update_keywords()
KEYWORDS_CSV = Path("data/sample_keywords.csv")
df_keywords = pd.read_csv(KEYWORDS_CSV)

# -----------------------------
# Streamlit UI
st.set_page_config(page_title="TrendRunner Designer", layout="centered")
st.title("🏃 TrendRunner Designer")
st.write("Generate trendy running T-shirt designs with AI-generated slogans!")

# Sidebar for settings
st.sidebar.header("Design Settings")

# Number of icons per design
num_icons = st.sidebar.slider("Number of icons per design", min_value=1, max_value=5, value=2)

# Font size range
font_size = st.sidebar.slider("Font size", min_value=20, max_value=50, value=30)

# Background color
bg_color = st.sidebar.color_picker("Background color", "#ffffff")

# Generate button
if st.sidebar.button("Generate Design"):

    # Choose a random keyword
    keyword_row = df_keywords.sample(n=1).iloc[0]
    keyword = keyword_row['keyword']
    popularity = keyword_row['popularity_last_month']
    st.write(f"**Keyword:** {keyword} (popularity: {popularity})")

    # Generate slogans using LLM
    slogans = generate_slogan(keyword, n=3)
    slogan = random.choice(slogans)
    st.write(f"**Slogan:** {slogan}")

    # Generate T-shirt design
    design_img = generate_design_image(
        slogan,
        num_icons=num_icons,
        font_size=font_size,
        bg_color=bg_color
    )

    # Display design
    st.image(design_img, caption="Generated T-shirt Design", width="stretch")
