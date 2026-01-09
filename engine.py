import pandas as pd
from ta.momentum import RSIIndicator, WilliamsRIndicator
from data import fetch_price, fetch_fundamentals

# ---------- helper ----------
def series(x):
    if isinstance(x, pd.DataFrame):
        x = x.iloc[:, 0]
    if isinstance(x, pd.Series):
        return x.squeeze()
    return pd.Series(x).squeeze()

# -------------------------
# MARKET REGIME
# -------------------------
def market_regime():
    df, _ = fetch_price("^NSEI")
    if df is None or len(df) < 50:
        return "UNKNOWN"

    rsi = RSIIndicator(series(df["Close"]), 14).rsi().iloc[-1]

    if rsi >= 50:
        return "RISK ON"
    elif rsi >= 40:
        return "NEUTRAL"
    else:
        return "RISK OFF"

# -------------------------
# BUY-READY SCANNER
# -------------------------
def buy_ready(symbol, sector_symbol):
    try:
        df, _ = fetch_price(symbol)
        sec, _ = fetch_price(sector_symbol)

        if df is None or sec is None or len(df) < 50:
            return None

        close = series(df["Close"])
        high = series(df["High"])
        low = series(df["Low"])

        rsi = RSIIndicator(close, 14).rsi()
        willr = WilliamsRIndicator(high, low, close, 14).williams_r()
        sec_rsi = RSIIndicator(series(sec["Close"]), 14).rsi()

        if (
            35 <= rsi.iloc[-1] <= 50 and
            rsi.iloc[-1] > rsi.iloc[-2] and
            willr.iloc[-2] < -80 and willr.iloc[-1] > -78 and
            sec_rsi.iloc[-1] > 50
        ):
            return {
                "Symbol": symbol,
                "RSI": round(rsi.iloc[-1], 2),
                "Decision": "BUY NOW",
                "Reason": "Momentum recovery with market support"
            }
        return None
    except Exception:
        return None

# -------------------------
# WATCHLIST
# -------------------------
def watchlist(symbol):
    try:
        df, _ = fetch_price(symbol)
        if df is None or len(df) < 50:
            return None

        rsi = RSIIndicator(series(df["Close"]), 14).rsi()

        if 30 <= rsi.iloc[-1] <= 45 and rsi.iloc[-1] > rsi.iloc[-2]:
            return {
                "Symbol": symbol,
                "RSI": round(rsi.iloc[-1], 2),
                "Note": "RSI improving"
            }
        return None
    except Exception:
        return None

# -------------------------
# RSI + WILLIAMS %R
# -------------------------
def rsi_willr(symbol):
    try:
        df, _ = fetch_price(symbol)
        if df is None or len(df) < 50:
            return None

        close = series(df["Close"])
        high = series(df["High"])
        low = series(df["Low"])

        rsi = RSIIndicator(close, 14).rsi()
        willr = WilliamsRIndicator(high, low, close, 14).williams_r()

        if (
            25 <= rsi.iloc[-1] <= 40 and
            rsi.iloc[-1] > rsi.iloc[-2] and
            willr.iloc[-2] < -80 and willr.iloc[-1] > -78
        ):
            return {
                "Symbol": symbol,
                "RSI": round(rsi.iloc[-1], 2),
                "Signal": "EARLY REVERSAL"
            }
        return None
    except Exception:
        return None

# -------------------------
# SYED ABDHAHEER PICKS (STRICT)
# -------------------------
def syed_pick(symbol):
    try:
        df, _ = fetch_price(symbol)
        f = fetch_fundamentals(symbol)

        if df is None or not f:
            return None

        rsi = RSIIndicator(series(df["Close"]), 14).rsi().iloc[-1]

        if not f.get("low52") or not f.get("price"):
            return None

        up = (f["price"] - f["low52"]) / f["low52"] * 100

        if (
            10 < rsi < 40 and
            f["marketCap"] > 10000 and
            f["debtToEquity"] is not None and f["debtToEquity"] < 1 and
            f["roe"] and f["roe"] > 0.15 and
            f["roa"] and f["roa"] > 0.05 and
            10 < up < 30
        ):
            return {
                "Symbol": symbol,
                "RSI": round(rsi, 2),
                "Tag": "SYED PICK"
            }
        return None
    except Exception:
        return None

# -------------------------
# TRADITIONAL SUGGESTIONS (BALANCED FUNDAMENTALS)
# -------------------------
def traditional_pick(symbol):
    try:
        f = fetch_fundamentals(symbol)
        if not f:
            return None

        pe = f.get("pe")
        earnings_growth = f.get("earningsGrowth")
        revenue_growth = f.get("revenueGrowth")

        growth_ok = (
            (earnings_growth and earnings_growth > 0.08) or
            (revenue_growth and revenue_growth > 0.08)
        )

        if (
            f["marketCap"] > 5000 and
            f["roe"] and f["roe"] > 0.12 and
            f["debtToEquity"] is not None and f["debtToEquity"] < 1 and
            pe and 8 <= pe <= 30 and
            growth_ok
        ):
            return {
                "Symbol": symbol,
                "ROE (%)": round(f["roe"] * 100, 1),
                "Debt/Equity": round(f["debtToEquity"], 2),
                "PE": round(pe, 1),
                "Tag": "Traditional Quality"
            }
        return None
    except Exception:
        return None
