from flask import Blueprint, redirect, request, render_template 
from interfaces import api_controller

analysis_bp = Blueprint("analysis", __name__, url_prefix="/analysis")

@analysis_bp.route("/")
def home_page():

    


    return None 
