-- Warehouse Schema
-- Clean, transformed data lives here
-- This is what Power BI reads from

-- Dimension table: coins
CREATE TABLE IF NOT EXISTS warehouse.dim_coin (
    coin_id         SERIAL PRIMARY KEY,
    coin_key        VARCHAR(50) UNIQUE NOT NULL,
    coin_name       VARCHAR(100),
    symbol          VARCHAR(20)
);

-- Dimension table: dates
CREATE TABLE IF NOT EXISTS warehouse.dim_date (
    date_key        SERIAL PRIMARY KEY,
    full_date       DATE UNIQUE NOT NULL,
    year            INTEGER,
    month           INTEGER,
    month_name      VARCHAR(20),
    day             INTEGER,
    day_of_week     VARCHAR(20),
    quarter         INTEGER
);

-- Fact table: crypto prices
CREATE TABLE IF NOT EXISTS warehouse.fact_crypto_prices (
    id              SERIAL PRIMARY KEY,
    coin_id         INTEGER REFERENCES warehouse.dim_coin(coin_id),
    date_key        INTEGER REFERENCES warehouse.dim_date(date_key),
    current_price   NUMERIC(20, 8),
    market_cap      NUMERIC(30, 2),
    total_volume    NUMERIC(30, 2),
    price_change_24h NUMERIC(20, 8),
    price_change_pct_24h NUMERIC(10, 4),
    loaded_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);