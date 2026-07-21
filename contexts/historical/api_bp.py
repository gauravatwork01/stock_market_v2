
from .app.services import HistoricalAppService
from flask import Blueprint, redirect, request, render_template 


historical_bp = Blueprint("historical", __name__, url_prefix="/historical")


@historical_bp.route("/sync", endpoint='sync')
def get_holdings():    
    return render_template("portfolio.html", holdings=[])


@historical_bp.route("/get", endpoint='get')
def get_holdings():    
    data = HistoricalAppService().get_historicals()
    return render_template("portfolio.html", holdings=[])

























