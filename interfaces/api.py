from flask import Blueprint, redirect, request, render_template 
# from interfaces import controller

# from app.services.vendor_auth_app_service import VendorAuthApplicationService
# from app.services.portfolio_app_service import PortfolioApplicationService
# from app.services.instruments_app_service import InstrumentsApplicationService
# from interfaces.auth_decorator import app_authentication_required
from interfaces import api_controller

api_bp = Blueprint("api", __name__)

@api_bp.route("/")
def home_page():
    return redirect("/auth/vendor_login")

@api_bp.route("/auth/vendor_login")
def vendor_login():
    login_url = api_controller.get_kite_login_url()
    return redirect(login_url)



@api_bp.route("/auth/vendor_request_token")
def vendor_request_token():
    request_token= request.args.get("request_token")
    api_controller.fetch_and_store_token(request_token)
    
    return redirect("/holdings")



@api_bp.route("/stock_listing", endpoint="stock_listing")
@api_controller.app_authentication_required
def portfolio():    
    stocks = InstrumentsApplicationService.get_all_stocks()
    return render_template("stocks_listing.html", stocks = stocks)



@api_bp.route("/holdings")
@api_controller.app_authentication_required
def holdings():    
    holdings = api_controller.get_holdings()
    return render_template("portfolio.html", holdings = holdings)


