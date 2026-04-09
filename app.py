import json
import os

import requests
from flask import Flask, Response, render_template

STOCK_API_BASE = os.environ.get(
    "STOCK_API_BASE", "https://stocks3.onrender.com"
).rstrip("/")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
