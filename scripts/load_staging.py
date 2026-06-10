import json
import os
import glob
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Build the connection string
if DB_PASSWORD:
    CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    CONNECTION_STRING = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_latest_raw_file():
    """Find the most recently created raw JSON file"""
    files = glob.glob("data/raw/crypto_*.json")
    if not files:
        print("No raw files found.")
        return None
    latest = max(files, key=os.path.getctime)
    return latest


def load_staging(data=None):
    print(f"[{datetime.now()}] Starting staging load...")

    # If no data passed in, read from the latest raw file
    if data is None:
        latest_file = get_latest_raw_file()
        if not latest_file:
            return
        print(f"[{datetime.now()}] Reading from {latest_file}")
        with open(latest_file, "r") as f:
            data = json.load(f)

    engine = create_engine(CONNECTION_STRING)

    insert_query = text("""
        INSERT INTO staging.crypto_prices (
            coin_id,
            coin_name,
            symbol,
            current_price,
            market_cap,
            total_volume,
            price_change_24h,
            price_change_pct_24h,
            last_updated
        )
        VALUES (
            :coin_id,
            :coin_name,
            :symbol,
            :current_price,
            :market_cap,
            :total_volume,
            :price_change_24h,
            :price_change_pct_24h,
            :last_updated
        )
    """)

    rows_loaded = 0

    with engine.connect() as conn:
        for coin in data:
            conn.execute(insert_query, {
                "coin_id":             coin["id"],
                "coin_name":           coin["name"],
                "symbol":              coin["symbol"],
                "current_price":       coin["current_price"],
                "market_cap":          coin["market_cap"],
                "total_volume":        coin["total_volume"],
                "price_change_24h":    coin["price_change_24h"],
                "price_change_pct_24h": coin["price_change_percentage_24h"],
                "last_updated":        coin["last_updated"]
            })
            rows_loaded += 1
        conn.commit()

    print(f"[{datetime.now()}] Loaded {rows_loaded} rows into staging.crypto_prices")


if __name__ == "__main__":
    load_staging()