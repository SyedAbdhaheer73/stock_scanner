import streamlit as st
import pandas as pd
import time
from universe import load_nifty200, SECTOR_INDEX_MAP
from engine import (
    market_regime,
    buy_ready,
    syed_pick,
    watchlist,
    traditional_pick,
    rsi_willr
)
from data import fetch_price

st.set_page_config(layout="wide")
st.title("📊 Stock Scanner & Decision Engine")

# -------- LOAD UNIVERSE --------
@st.cache_data(ttl=24 * 60 * 60)
def get_universe():
    return load_nifty200()

UNIVERSE = get_universe()
st.caption(f"Universe size: {len(UNIVERSE)} stocks")

# -------- DATA FRESHNESS --------
_, market_ts = fetch_price("^NSEI")
if market_ts:
    st.caption(f"🕒 Market data last fetched at: {market_ts.strftime('%Y-%m-%d %H:%M:%S')}")

# -------- MARKET REGIME --------
regime = market_regime()
st.markdown(f"### 🧭 Market Regime: **{regime}**")

buy, syed, watch, traditional, early = [], [], [], [], []

progress = st.progress(0)
status = st.empty()
start_time = time.time()

stocks = list(UNIVERSE.items())
total = len(stocks)

with st.spinner("Scanning stocks..."):
    for i, (stock, sector) in enumerate(stocks):
        progress.progress((i + 1) / total)
        status.text(f"Scanning {stock} ({i+1}/{total})")

        sector_symbol = SECTOR_INDEX_MAP.get(sector)

        if sector_symbol:
            r = buy_ready(stock, sector_symbol)
            if r:
                buy.append(r)

        s = syed_pick(stock)
        if s:
            syed.append(s)

        w = watchlist(stock)
        if w:
            watch.append(w)

        t = traditional_pick(stock)
        if t:
            traditional.append(t)

        e = rsi_willr(stock)
        if e:
            early.append(e)

progress.empty()
status.empty()

elapsed = round(time.time() - start_time, 1)
st.caption(f"⏱ Scan completed in {elapsed} seconds")

# -------- DISPLAY --------
def show(title, data, empty):
    st.subheader(title)
    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    else:
        st.info(empty)

show("🟢 Buy-Ready Scanner", buy, "No buy-ready setups today.")
show("⭐ Syed Abdhaheer’s Picks", syed, "No Syed Picks today.")
show("🟡 Watchlist Candidates", watch, "No watchlist candidates today.")
show("🟣 Traditional Suggestions", traditional, "No traditional quality picks today.")
show("🔵 RSI + Williams %R Early Signals", early, "No early reversal signals today.")
