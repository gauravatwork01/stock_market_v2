import json
import os
import requests
from flask import Flask, Response, redirect, render_template, url_for, request
from src.broker.kite_connect.auth.service import VendorAPIClientService, VendorAuthFlowService
from src.broker.kite_connect.portfolio.service import PortfolioService
from utilities import utilities
from google.cloud import bigquery

app = Flask(__name__)

@app.route("/app")
def stock_app():
    return render_template("home.html")


@app.route("/")
def start_page():
    return redirect(url_for("home_page_endpoint"))


@app.route("/home", endpoint="home_page_endpoint")
def home_page():
    is_online = VendorAuthFlowService.is_online()
    if is_online:
        holdings = PortfolioService.get_holdings()
        return render_template("home.html", is_online= is_online, holdings= holdings)
    else:
        return redirect(url_for("vendor_login_endpoint"))


@app.route("/vendor_login", endpoint="vendor_login_endpoint")
def vendor_login():
    login_url = VendorAPIClientService.get_login_url()
    return redirect(login_url)

@app.route("/vendor_request_token", endpoint="vendor_request_token")
def vendor_token():
    vendor_request_token = request.args.get("request_token")
    vendor_access_token = VendorAPIClientService.get_access_token(
        request_token= vendor_request_token
    )
    # vendor_access_token = {}
    # vendor_access_token["access_token"] = "98hujiop"
    current_date = utilities.get_ist_date()
    VendorAuthFlowService.save_token(
        token_date = current_date,
        request_token = vendor_request_token,
        access_token = vendor_access_token["access_token"]
    )
    VendorAPIClientService.attach_access_token(
        access_token= vendor_access_token["access_token"]
    )
    return redirect(url_for("home_page_endpoint"))


# VendorAPIClientService.attach_access_token(
#     access_token= "iHJsvotQZrdYvBHHKH6uAn6v5pH1aUhZ"
# )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), debug=True)
