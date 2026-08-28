from flask import Blueprint, request, render_template
# from .services.upload_services import upload_financials 
# from .api_controller import upload_financials
from . import api_controller

financials_bp = Blueprint("financials", __name__, url_prefix="/financials")




@financials_bp.route("/xlsx_upload", endpoint="home", methods=["POST"])
def upload():

    api_controller.upload_financials(request)
    

    return {"status": "success"}, 200




@financials_bp.route("/xbrl_upload", endpoint="xbrl_upload", methods=["POST"])
def upload_xbrl():
    api_controller.ingest_xbrl_filings(request)
    return {"status": "success"}, 200


@financials_bp.route("/get", endpoint="get", methods=["POST"])
def get_financials():
    request_json = request.get_json(silent=True) or {}
    isin = request_json.get("isin")
    data = api_controller.get_financials(isin)
    return data, 200












