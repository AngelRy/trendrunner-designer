# image_gen.py
from PIL import Image, ImageDraw, ImageFont
import random
import os
import textwrap

# Fonts directory and available fonts
FONTS_DIR = "/usr/share/fonts/truetype/dejavu/"
AVAILABLE_FONTS = ["DejaVuSans-Bold.ttf", "DejaVuSerif-Bold.ttf"]

# Icons folder
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(PROJECT_ROOT, "icons")
os.makedirs(ICONS_DIR, exist_ok=True)  # ensure folder exists
ICON_FILES = [f for f in os.listdir(ICONS_DIR) if f.endswith(".png")]

def random_font(font_size=30):
    font_file = random.choice(AVAILABLE_FONTS)
    font_path = os.path.join(FONTS_DIR, font_file)
    return ImageFont.truetype(font_path, font_size)

def generate_design_image(slogan, num_icons=2, font_size=30, bg_color="white"):
    # 1️⃣ Background
    img = Image.new("RGB", (400, 400), color=bg_color)
    draw = ImageDraw.Draw(img)

    # 2️⃣ Random shapes for flair
    for _ in range(random.randint(1, 3)):
        shape_type = random.choice(["circle", "rectangle", "triangle", "none"])
        color = random.choice(["red", "blue", "green", "orange", "purple", "pink", "yellow"])
        x, y = random.randint(20, 250), random.randint(20, 250)
        size = random.randint(50, 120)

        if shape_type == "circle":
            draw.ellipse((x, y, x + size, y + size), fill=color)
        elif shape_type == "rectangle":
            draw.rectangle((x, y, x + size, y + size), fill=color)
        elif shape_type == "triangle":
            points = [(x, y), (x + size, y), (x + size // 2, y + size)]
            draw.polygon(points, fill=color)

    # 3️⃣ Add multiple random icons
    if ICON_FILES:
        for _ in range(num_icons):
            icon_file = random.choice(ICON_FILES)
            icon = Image.open(os.path.join(ICONS_DIR, icon_file)).convert("RGBA")
            # Resize icon randomly
            scale = random.uniform(0.5, 1.2)
            w, h = icon.size
            icon = icon.resize((int(w * scale), int(h * scale)))
            # Random position
            x, y = random.randint(0, 300), random.randint(0, 300)
            img.paste(icon, (x, y), icon)

    # 4️⃣ Slogan text with wrapping and centering
    font = random_font(font_size)
    max_width = 360  # leave some padding
    lines = textwrap.wrap(slogan, width=15)  # wrap lines

    # Compute total text height
    total_text_height = 0
    line_sizes = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        line_sizes.append((w, h))
        total_text_height += h

    y_start = (img.height - total_text_height) // 2

    # Draw each line centered
    for idx, line in enumerate(lines):
        w, h = line_sizes[idx]
        x = (img.width - w) // 2
        draw.text(
            (x, y_start),
            line,
            font=font,
            fill=random.choice(["black", "darkblue", "darkred", "white"])
        )
        y_start += h

    # 5️⃣ Optional rotation
    img = img.rotate(random.randint(-10, 10), expand=1, fillcolor=bg_color)

    return img
