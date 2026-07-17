from flask import Blueprint, redirect, request, render_template 
# from interfaces import api_controller
from contexts.broker_auth.application.services import kite_authentication_required

holdings_bp = Blueprint("holdings", __name__, url_prefix="/holdings")




@holdings_bp.route("/")
@kite_authentication_required
def holdings():    
    holdings = api_controller.get_holdings()
    return render_template("portfolio.html", holdings = holdings)














