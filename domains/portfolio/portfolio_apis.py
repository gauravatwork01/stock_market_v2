
from domains.portfolio.portfolio_services import PortfolioService
from flask import Flask, Response, redirect, render_template, url_for, request, Blueprint

portfolio_bp = Blueprint("portfolio", __name__, url_prefix="/portfolio")




@portfolio_bp.route("/", endpoint="portfolio_endpoint")
def home_page():
    is_app_authenticated = True 
    holdings = PortfolioService.get_holdings()
    return render_template("home.html", is_app_authenticated= is_app_authenticated, holdings= holdings)




