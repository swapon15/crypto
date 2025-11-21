from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Cache last good price
last_price = 0

def fetch_btc_price(retries=3):
    global last_price
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            price = data.get("bitcoin", {}).get("usd")
            if price is not None:
                last_price = price
                return price
        except:
            pass  # try again

    # If all retries fail, return last known good price
    return last_price

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/price")
def price():
    return jsonify({"price": fetch_btc_price()})

if __name__ == "__main__":
    app.run(debug=True)
