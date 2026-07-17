
from flask import Blueprint, redirect, request, render_template 
from interfaces import api_controller

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/")
def home_page():

    


    return None 





