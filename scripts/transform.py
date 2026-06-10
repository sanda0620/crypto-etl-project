import os
from datetime import datetime, date
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if DB_PASSWORD:
    CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    CONNECTION_STRING = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def load_dim_coin(conn):
    """Insert new coins into dim_coin — skip if already exists"""
    print(f"[{datetime.now()}] Loading dim_coin...")

    query = text("""
        INSERT INTO warehouse.dim_coin (coin_key, coin_name, symbol)
        SELECT DISTINCT coin_id, coin_name, symbol
        FROM staging.crypto_prices
        ON CONFLICT (coin_key) DO NOTHING
    """)

    conn.execute(query)
    print(f"[{datetime.now()}] dim_coin loaded.")


def load_dim_date(conn):
    """Insert today's date into dim_date — skip if already exists"""
    print(f"[{datetime.now()}] Loading dim_date...")

    today = date.today()

    query = text("""
        INSERT INTO warehouse.dim_date (
            full_date, year, month, month_name, day, day_of_week, quarter
        )
        VALUES (
            :full_date, :year, :month, :month_name, :day, :day_of_week, :quarter
        )
        ON CONFLICT (full_date) DO NOTHING
    """)

    conn.execute(query, {
        "full_date":    today,
        "year":         today.year,
        "month":        today.month,
        "month_name":   today.strftime("%B"),
        "day":          today.day,
        "day_of_week":  today.strftime("%A"),
        "quarter":      (today.month - 1) // 3 + 1
    })

    print(f"[{datetime.now()}] dim_date loaded.")


def load_fact_crypto_prices(conn):
    """Load latest staging data into fact table"""
    print(f"[{datetime.now()}] Loading fact_crypto_prices...")

    query = text("""
        INSERT INTO warehouse.fact_crypto_prices (
            coin_id,
            date_key,
            current_price,
            market_cap,
            total_volume,
            price_change_24h,
            price_change_pct_24h
        )
        SELECT
            dc.coin_id,
            dd.date_key,
            sp.current_price,
            sp.market_cap,
            sp.total_volume,
            sp.price_change_24h,
            sp.price_change_pct_24h
        FROM staging.crypto_prices sp
        JOIN warehouse.dim_coin dc ON dc.coin_key = sp.coin_id
        JOIN warehouse.dim_date dd ON dd.full_date = CURRENT_DATE
        WHERE sp.loaded_at = (
            SELECT MAX(loaded_at) FROM staging.crypto_prices
        )
    """)

    conn.execute(query)
    print(f"[{datetime.now()}] fact_crypto_prices loaded.")


def transform():
    print(f"[{datetime.now()}] Starting transformation...")

    engine = create_engine(CONNECTION_STRING)

    with engine.connect() as conn:
        load_dim_coin(conn)
        load_dim_date(conn)
        load_fact_crypto_prices(conn)
        conn.commit()

    print(f"[{datetime.now()}] Transformation complete.")


if __name__ == "__main__":
    transform()