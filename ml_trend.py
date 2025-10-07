# ml_trend.py
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Sample keyword trends (month vs popularity)
data = pd.DataFrame({
    'keyword': ['marathon', 'recovery', 'grit', 'ultra', 'trail'],
    'popularity_last_month': [80, 60, 70, 50, 40]
})

# For simplicity: predict next month popularity as linear trend
def predict_trend(keyword):
    if keyword not in data['keyword'].values:
        return 50  # default popularity
    val = data.loc[data['keyword']==keyword, 'popularity_last_month'].values[0]
    # simple growth assumption
    predicted = val + np.random.randint(-5,10)
    return min(max(predicted, 0), 100)  # clamp between 0-100
