import json
import os
from services import application
import requests
from flask import Flask, Response, redirect, render_template, url_for, request

STOCK_API_BASE = os.environ.get(
    "STOCK_API_BASE", "https://stocks3.onrender.com"
).rstrip("/")


from google.cloud import bigquery
bq_client = bigquery.Client() 

app = Flask(__name__)
app.bq_client = bq_client

@app.route("/app")
def stock_app():
    return render_template("index.html")


@app.route("/")
def index():
    return redirect(url_for("kite_login_url"))


@app.route("/vendor_login", endpoint="kite_login_url")
def vendor_login():
    kite_app_api_key = "qjj8i06fi5r3s8ru"
    kite_public_login_endpoint = f"https://kite.zerodha.com/connect/login?v=3&api_key={kite_app_api_key}"
    return redirect(kite_public_login_endpoint)


@app.route("/vendor_token", endpoint="vendor_token")
def vendor_token():
    vendor_request_token = request.args.get("request_token")
    application.save_vendor_token(
        req_token = vendor_request_token
    )
    print(f"vendor_request_token is {vendor_request_token}")
    return f"req-token recd is {vendor_request_token}"


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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), debug=True)
