import json
import os
import requests
from flask import Flask, Response, redirect, render_template, url_for, request
# from src.broker.kite_connect.auth.service import VendorAPIClientService, VendorAuthFlowService
# from src.broker.kite_connect.portfolio.service import PortfolioService
from utilities import utilities
from google.cloud import bigquery
from domains.vendor_auth.auth_services import VendorAuthFlowService

from domains.vendor_auth.auth_apis import auth_bp
from domains.portfolio.portfolio_apis import portfolio_bp

app = Flask(__name__)

@app.route("/", endpoint="home_page_endpoint")
def home_page():
    is_app_authenticated = VendorAuthFlowService.is_app_authenticated() 
    if is_app_authenticated is True:
        return redirect(url_for("portfolio.portfolio_endpoint"))
    else:
        return redirect(url_for("auth.vendor_login_endpoint"))

app.register_blueprint(auth_bp)
app.register_blueprint(portfolio_bp)

@app.before_request
def auth_middleware():
    if request.path.startswith("/auth"):
        return
    else:
        if VendorAuthFlowService.is_app_authenticated() is False:
            return redirect(url_for("auth.vendor_login_endpoint"))





# @app.route("/home", endpoint="home_page_endpoint")
# def home_page():
#     is_app_authenticated = VendorAuthFlowService.is_app_authenticated()
#     if is_app_authenticated:
#         holdings = PortfolioService.get_holdings()
#         return render_template("home.html", is_app_authenticated= is_app_authenticated, holdings= holdings)
#     else:
#         return redirect(url_for("vendor_login_endpoint"))



# VendorAPIClientService.attach_access_token(
#     access_token= "iHJsvotQZrdYvBHHKH6uAn6v5pH1aUhZ"
# )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), debug=True)
