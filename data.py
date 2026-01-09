import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime

@st.cache_data(ttl=60 * 60)
def fetch_price(symbol, period="1y"):
    try:
        df = yf.download(symbol, period=period, progress=False)
        if df.empty:
            return None, None

        for col in ["Open", "High", "Low", "Close", "Volume"]:
            if col in df.columns and isinstance(df[col], pd.DataFrame):
                df[col] = df[col].iloc[:, 0]

        fetched_at = datetime.now()
        return df, fetched_at
    except Exception:
        return None, None

@st.cache_data(ttl=24 * 60 * 60)
def fetch_fundamentals(symbol):
    try:
        info = yf.Ticker(symbol).info
        return {
            "marketCap": (info.get("marketCap") or 0) / 1e7,
            "debtToEquity": info.get("debtToEquity"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "low52": info.get("fiftyTwoWeekLow"),
            "price": info.get("currentPrice"),
            "pe": info.get("trailingPE"),
            "earningsGrowth": info.get("earningsGrowth"),
            "revenueGrowth": info.get("revenueGrowth"),
            "fetched_at": datetime.now()
        }
    except Exception:
        return {}
