import json
import os
import requests
from flask import Flask, Response, redirect, render_template, url_for, request
from src.broker.kite_connect.auth.service import KiteConnectService, VendorAuthService
from utilities import utilities

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
    login_url = KiteConnectService.get_login_url()
    return redirect(login_url)

@app.route("/vendor_request_token", endpoint="vendor_request_token")
def vendor_token():
    vendor_request_token = request.args.get("request_token")
    vendor_access_token = KiteConnectService.get_access_token(
        request_token= vendor_request_token
    )
    # vendor_access_token = {}
    # vendor_access_token["access_token"] = "98hujiop"
    current_date = utilities.get_ist_date()
    VendorAuthService.save_token(
        token_date = current_date,
        request_token = vendor_request_token,
        access_token = vendor_access_token["access_token"]
    )
    # return f"Done: vendor_access_token-{vendor_access_token['access_token']}"
    return f"Done: vendor_req_token-{vendor_request_token}"


# @app.route("/api/stocks/<path:endpoint>")
# def stocks_proxy(endpoint: str):
#     url = f"{STOCK_API_BASE}/api/stocks/{endpoint}"
#     try:
#         upstream = requests.get(url, timeout=60)
#     except requests.RequestException as exc:
#         return Response(
#             json.dumps(
#                 {"error": "upstream request failed", "detail": str(exc)}
#             ),
#             status=502,
#             mimetype="application/json",
#         )
#     ct = upstream.headers.get("content-type", "application/json")
#     return Response(upstream.content, status=upstream.status_code, mimetype=ct)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), debug=True)
