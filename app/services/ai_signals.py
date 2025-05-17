# app/services/ai_signals.py
import xgboost as xgb
import pandas as pd
import numpy as np
import os

# Load the model dynamically
MODEL_PATH = os.getenv("MODEL_PATH", "models/xgboost_model.pkl")
model = xgb.XGBClassifier()
model.load_model(MODEL_PATH)

def generate_signal(features: pd.DataFrame):
    """
    Generates a signal using the XGBoost model.
    :param features: A DataFrame containing the necessary features.
    :return: Tuple of (Signal Type, Confidence Level)
    """
    try:
        # Prediction
        prediction = model.predict(features)
        confidence = np.max(model.predict_proba(features), axis=1)[0] * 100

        # Determine signal type
        signal_type = "📈 Bullish" if prediction[0] == 1 else "📉 Bearish"
        return signal_type, round(confidence, 2)
    except Exception as e:
        print(f"Model prediction failed: {e}")
        return "⚠️ Error", 0.0
