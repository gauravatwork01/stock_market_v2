
from flask import Blueprint, redirect, request, render_template 
from interfaces import api_controller
from .application.services import get_kite_login_url



broker_auth_bp = Blueprint("broker_auth", __name__, url_prefix="/broker_auth")



# @broker_auth_bp.route("/")
# def home_page():
#     return redirect("/broker_auth/vendor_login")



@broker_auth_bp.route("/vendor_login", endpoint="login")
def vendor_login():
    # login_url = api_controller.get_kite_login_url()
    login_url = get_kite_login_url()
    return redirect(login_url)



@broker_auth_bp.route("/vendor_request_token")
def vendor_request_token():
    request_token= request.args.get("request_token")
    api_controller.fetch_and_store_token(request_token)
    
    return redirect("/holdings")










# @auth_bp.route("/")
# def home_page():

    


#     return None 





