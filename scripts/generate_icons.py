# scripts/generate_icons.py
from PIL import Image, ImageDraw
import os

# Get absolute path to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = os.path.join(PROJECT_ROOT, "icons")
os.makedirs(ICON_DIR, exist_ok=True)

# -----------------------------
# 1️⃣ Shoe-like icon
img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.ellipse((10, 30, 80, 70), fill="black")  # sole
draw.rectangle((20, 20, 70, 50), fill="black")  # upper
img.save(os.path.join(ICON_DIR, "shoe.png"))

# -----------------------------
# 2️⃣ Runner stick figure
img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.ellipse((40, 10, 60, 30), fill="black")       # head
draw.line((50, 30, 50, 70), fill="black", width=4)  # body
draw.line((50, 40, 30, 60), fill="black", width=3)  # left arm
draw.line((50, 40, 70, 60), fill="black", width=3)  # right arm
draw.line((50, 70, 30, 90), fill="black", width=3)  # left leg
draw.line((50, 70, 70, 90), fill="black", width=3)  # right leg
img.save(os.path.join(ICON_DIR, "runner1.png"))

# -----------------------------
# 3️⃣ Track lines
img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.line((20, 30, 80, 30), fill="black", width=4)
draw.line((20, 50, 80, 50), fill="black", width=4)
draw.line((20, 70, 80, 70), fill="black", width=4)
img.save(os.path.join(ICON_DIR, "track.png"))

print(f"✅ Sample icons generated in {ICON_DIR}")
