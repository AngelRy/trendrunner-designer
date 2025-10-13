import pandas as pd
import random
import time
from pathlib import Path
from pytrends.request import TrendReq

DATA_PATH = Path("data/sample_keywords.csv")

# Define your base keywords (can be extended dynamically)
BASE_KEYWORDS = [
    "running", "marathon", "trail running", "ultra running",
    "HIIT", "crossfit", "yoga", "recovery run", "stretching",
    "fitness", "interval training", "5K run", "10K run"
]

def fetch_trends(keywords):
    pytrend = TrendReq(hl="en-US", tz=360)
    records = []

    for kw in keywords:
        try:
            print(f"🌐 Fetching trend data for '{kw}'...")
            pytrend.build_payload([kw], timeframe="today 12-m")
            df = pytrend.interest_over_time()

            if not df.empty:
                popularity = int(df[kw].iloc[-1])
                print(f"✅ {kw}: {popularity}")
                records.append((kw, popularity))
            else:
                print(f"⚠️ No data for {kw}, using fallback value.")
                records.append((kw, random.randint(40, 90)))

            time.sleep(random.uniform(1.5, 3.5))  # avoid rate limits

        except Exception as e:
            print(f"❌ Error fetching {kw}: {e}")
            records.append((kw, random.randint(40, 90)))

    return pd.DataFrame(records, columns=["keyword", "popularity_last_month"])

def update_keywords():
    try:
        df = fetch_trends(BASE_KEYWORDS)
        df.to_csv(DATA_PATH, index=False)
        print(f"✅ Trend data saved to {DATA_PATH}")
    except Exception as e:
        print(f"💡 Using static fallback due to error: {e}")
        df = pd.DataFrame({
            "keyword": BASE_KEYWORDS,
            "popularity_last_month": [random.randint(40, 90) for _ in BASE_KEYWORDS]
        })
        df.to_csv(DATA_PATH, index=False)
        print(f"✅ Fallback keywords saved to {DATA_PATH}")

if __name__ == "__main__":
    update_keywords()
