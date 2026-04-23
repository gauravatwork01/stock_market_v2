from flask import Blueprint, redirect, request, render_template 
# from interfaces import controller

from app.services.vendor_auth_app_service import VendorAuthApplicationService
from app.services.portfolio_app_service import PortfolioApplicationService
# from app.


api_bp = Blueprint("api", __name__)

@api_bp.route("/")
def home_page():
    return redirect("/auth/vendor_login")

@api_bp.route("/auth/vendor_login")
def vendor_login():
    login_url = VendorAuthApplicationService.get_vendor_login_url()
    return redirect(login_url)


@api_bp.route("/auth/vendor_request_token")
def vendor_request_token():
    VendorAuthApplicationService.fetch_and_store_access_token(
        request_token= request.args.get("request_token")
    )
    return redirect("/portfolio")


@api_bp.route("/portfolio")
def portfolio():
    # VendorAuthAppService.fetch_and_store_access_token()
    holdings = PortfolioApplicationService.get_holdings()
    return render_template("portfolio.html", holdings = holdings)

