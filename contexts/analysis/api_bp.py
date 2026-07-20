
from flask import Blueprint, redirect, request, render_template 
# from interfaces import api_controller
# from .application.services import get_kite_login_url



analysis_bp = Blueprint("analysis_bp", __name__, url_prefix="/analysis")


@analysis_bp.route("/", endpoint="home")
def analysis_home():
    
    return None 




