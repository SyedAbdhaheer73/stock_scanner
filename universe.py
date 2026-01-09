import pandas as pd

# Fallback index when sector is unknown
DEFAULT_INDEX = "^NSEI"   # NIFTY 50 as proxy

SECTOR_INDEX_MAP = {
    "DEFAULT": DEFAULT_INDEX
}

def load_nifty200(csv_path="universe/MW-NIFTY-200-10-Jan-2026.csv"):
    df = pd.read_csv(csv_path)

    # Normalize column names (strip whitespace & newlines)
    df.columns = [c.strip() for c in df.columns]

    if "SYMBOL" not in df.columns:
        raise ValueError(f"SYMBOL column not found. Columns: {df.columns.tolist()}")

    universe = {}

    for _, row in df.iterrows():
        symbol = str(row["SYMBOL"]).strip()

        if not symbol or symbol.lower() == "nan":
            continue

        # NSE symbol format
        nse_symbol = symbol + ".NS"

        # Sector unknown → use default index
        universe[nse_symbol] = "DEFAULT"

    return universe
