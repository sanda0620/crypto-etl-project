import requests
import json
import os
from datetime import datetime

# CoinGecko API endpoint
# We are fetching market data for 5 major coins in USD
URL = "https://api.coingecko.com/api/v3/coins/markets"

PARAMS = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,solana,binancecoin,cardano",
    "order": "market_cap_desc",
    "per_page": 5,
    "page": 1,
    "sparkline": False
}

def extract():
    print(f"[{datetime.now()}] Starting extraction...")

    response = requests.get(URL, params=PARAMS)

    # Check if the API call was successful
    if response.status_code != 200:
        print(f"API call failed. Status code: {response.status_code}")
        return None

    data = response.json()

    # Save raw response to data/raw/ with a timestamp in the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/raw/crypto_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[{datetime.now()}] Extracted {len(data)} coins.")
    print(f"[{datetime.now()}] Raw data saved to {filename}")

    return data

if __name__ == "__main__":
    extract()