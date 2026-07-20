from flask import Blueprint, redirect, request, render_template 

holdings_bp = Blueprint("holdings", __name__, url_prefix="/holdings")




@holdings_bp.route("/", endpoint='home')
def get_holdings():    
    return render_template("portfolio.html", holdings=[])














