from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

def fetch_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd"}
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        return data["bitcoin"]["usd"]
    except Exception as e:
        # keep simple: return None on error
        return {"error": str(e)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/price")
def price():
    return jsonify({"price": fetch_btc_price()})

if __name__ == "__main__":
    app.run(debug=True)
