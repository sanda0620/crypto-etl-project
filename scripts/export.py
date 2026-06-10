import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine

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


def export():
    print(f"[{datetime.now()}] Starting export...")

    engine = create_engine(CONNECTION_STRING)

    # Export fact table with joined dim data — this is what Power BI reads
    fact_query = """
        SELECT
            dc.coin_key,
            dc.coin_name,
            dc.symbol,
            dd.full_date,
            dd.year,
            dd.month,
            dd.month_name,
            dd.day,
            dd.day_of_week,
            dd.quarter,
            f.current_price,
            f.market_cap,
            f.total_volume,
            f.price_change_24h,
            f.price_change_pct_24h,
            f.loaded_at
        FROM warehouse.fact_crypto_prices f
        JOIN warehouse.dim_coin dc ON dc.coin_id = f.coin_id
        JOIN warehouse.dim_date dd ON dd.date_key = f.date_key
        ORDER BY dd.full_date DESC, f.market_cap DESC
    """

    dim_coin_query = "SELECT * FROM warehouse.dim_coin ORDER BY coin_id"
    dim_date_query = "SELECT * FROM warehouse.dim_date ORDER BY full_date"

    # Read into dataframes
    df_fact = pd.read_sql(fact_query, engine)
    df_coin = pd.read_sql(dim_coin_query, engine)
    df_date = pd.read_sql(dim_date_query, engine)

    # Save to exports/
    df_fact.to_csv("exports/fact_crypto_prices.csv", index=False)
    df_coin.to_csv("exports/dim_coin.csv", index=False)
    df_date.to_csv("exports/dim_date.csv", index=False)

    print(f"[{datetime.now()}] Exported {len(df_fact)} rows to exports/fact_crypto_prices.csv")
    print(f"[{datetime.now()}] Exported {len(df_coin)} rows to exports/dim_coin.csv")
    print(f"[{datetime.now()}] Exported {len(df_date)} rows to exports/dim_date.csv")
    print(f"[{datetime.now()}] Export complete.")


if __name__ == "__main__":
    export()