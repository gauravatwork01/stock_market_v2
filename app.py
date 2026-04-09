import json
import os

import requests
from flask import Flask, Response, render_template, redirect

STOCK_API_BASE = os.environ.get(
    "STOCK_API_BASE", "https://stocks3.onrender.com"
).rstrip("/")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/kite")
def kite_login():
    kite_app_api_key = "qjj8i06fi5r3s8ru"
    kite_public_login_endpoint = f"https://kite.zerodha.com/connect/login?v=3&api_key={kite_app_api_key}"
    return redirect(kite_public_login_endpoint)

@app.route("/api/stocks/<path:endpoint>")
def stocks_proxy(endpoint: str):
    url = f"{STOCK_API_BASE}/api/stocks/{endpoint}"
    try:
        upstream = requests.get(url, timeout=60)
    except requests.RequestException as exc:
        return Response(
            json.dumps(
                {"error": "upstream request failed", "detail": str(exc)}
            ),
            status=502,
            mimetype="application/json",
        )
    ct = upstream.headers.get("content-type", "application/json")
    return Response(upstream.content, status=upstream.status_code, mimetype=ct)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)
