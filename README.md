[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-app-orange)](https://streamlit.io)
[![License](https://img.shields.io/github/license/SyedAbdhaheer73/stock_scanner)](LICENSE)


# 📊 Stock Scanner & Decision Engine

A rule-based **decision-support system** for Indian equities using
**technical + fundamental analysis**.

---

## 🚀 Features
- Live (Yahoo Finance) data
- Market regime filter
- Buy-ready momentum scanner
- Strict personal strategy (Syed Abdhaheer’s Picks)
- Watchlist builder
- Traditional quality investing filter
- RSI + Williams %R early signals
- NIFTY 200 universe
- Caching for speed & rate-limit safety

---

## 🗂 Project Structure

stock_scanner/
├── app.py
├── engine.py
├── data.py
├── universe.py
├── universe/
│   └── MW-NIFTY-200-10-Jan-2026.csv
├── requirements.txt
├── README.md
└── .gitignore

---

## ▶️ How to Run

1. Create virtual environment

python3 -m venv venv  
source venv/bin/activate

2. Install dependencies

python3 -m pip install -r requirements.txt

3. Run the app (IMPORTANT)

streamlit run app.py

---

## 🧭 Sections Explained

🟢 **Buy-Ready Scanner**  
Actionable momentum setups aligned with market regime

⭐ **Syed Abdhaheer’s Picks**  
Strict high-conviction strategy using technical + fundamental filters

🟡 **Watchlist Candidates**  
Stocks showing early momentum improvement

🟣 **Traditional Suggestions**  
Moderate fundamental quality filter (long-term style)

🔵 **RSI + Williams %R Early Signals**  
Early reversal signals for preparation

---

## 🕒 Data Freshness
- Price data: Yahoo Finance (near real-time / EOD)
- Fundamentals: Yahoo Finance (quarterly / annual)
- Cached to reduce API hits and speed up scans

---

## ⚠️ Disclaimer
For educational and personal analysis only.  
Not financial advice.

---

## 👤 Author
Syed Abdhaheer