-- Staging Schema
-- Raw data from CoinGecko API lands here first
-- No cleaning, no transformation, just raw dump

CREATE TABLE IF NOT EXISTS staging.crypto_prices (
    id              SERIAL PRIMARY KEY,
    coin_id         VARCHAR(50),
    coin_name       VARCHAR(100),
    symbol          VARCHAR(20),
    current_price   NUMERIC(20, 8),
    market_cap      NUMERIC(30, 2),
    total_volume    NUMERIC(30, 2),
    price_change_24h NUMERIC(20, 8),
    price_change_pct_24h NUMERIC(10, 4),
    last_updated    TIMESTAMP,
    loaded_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);