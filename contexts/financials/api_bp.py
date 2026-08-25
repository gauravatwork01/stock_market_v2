from flask import Blueprint, request, render_template
# from .services.upload_services import upload_financials 
# from .api_controller import upload_financials
from . import api_controller

financials_bp = Blueprint("financials", __name__, url_prefix="/financials")




@financials_bp.route("/upload", endpoint="home", methods=["POST"])
def upload():

    api_controller.upload_financials(request)

    return {"status": "success"}, 200














