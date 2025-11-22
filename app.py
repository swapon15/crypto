from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Cache last known good prices per coin (CoinGecko ids)
last_prices = {"ripple": 0.0, "cardano": 0.0, "dogecoin": 0.0}


def fetch_prices(coins=None, retries=3):
    """Fetch USD prices for the given CoinGecko ids.

    Returns a dict mapping coin id -> price (float) using cached last known
    values when live fetch fails.
    """
    global last_prices
    if coins is None:
        coins = ["ripple", "cardano", "dogecoin"]
    if isinstance(coins, str):
        coins = [c.strip() for c in coins.split(",") if c.strip()]

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(coins), "vs_currencies": "usd"}

    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            result = {}
            for coin in coins:
                price = data.get(coin, {}).get("usd")
                if price is not None:
                    last_prices[coin] = price
                result[coin] = last_prices.get(coin)

            return result
        except Exception:
            # try again
            pass

    # If all retries fail, return last known good prices for requested coins
    return {coin: last_prices.get(coin) for coin in coins}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/price")
def price():
    # Return a dynamic mapping of CoinGecko id -> price (USD).
    # Frontend will render whatever currency ids are returned here.
    prices = fetch_prices()
    return jsonify(prices)


if __name__ == "__main__":
    app.run(debug=True)
