# update_keywords.py
import os
import pandas as pd
import random

CSV_PATH = os.path.join("data", "sample_keywords.csv")

# Base keywords relevant to running & recovery
BASE_KEYWORDS = [
    "running", "marathon", "trail", "recovery", "ultra",
    "HIIT", "5K", "10K", "crossfit", "yoga", "fitness", "stretching"
]

def update_keywords():
    try:
        from pytrends.request import TrendReq
        print("🌐 Fetching Google Trends data...")
        pytrends = TrendReq(hl='en-US', tz=360)

        # Build payload
        pytrends.build_payload(BASE_KEYWORDS, timeframe='today 1-m', geo='US')
        data = pytrends.interest_over_time()
        
        if data.empty:
            raise Exception("No trend data received from Google.")

        # Extract last month popularity
        df = pd.DataFrame({
            "keyword": BASE_KEYWORDS,
            "popularity_last_month": [int(data[kw].iloc[-1]) for kw in BASE_KEYWORDS]
        })

        # Add slight random variation for demo appearance
        df["popularity_last_month"] = df["popularity_last_month"].apply(lambda x: max(1, x + random.randint(-10, 10)))
        df.to_csv(CSV_PATH, index=False)
        print(f"✅ Keywords updated from Google Trends at {CSV_PATH}")

    except Exception as e:
        print(f"⚠️ Could not fetch Google Trends: {e}")
        print("💡 Using dynamic fallback keywords")

        # Randomized popularity for fallback
        data = []
        for kw in BASE_KEYWORDS:
            popularity = random.randint(30, 100)
            data.append({"keyword": kw, "popularity_last_month": popularity})

        df = pd.DataFrame(data)
        os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
        df.to_csv(CSV_PATH, index=False)
        print(f"✅ Fallback keywords saved at {CSV_PATH}")
