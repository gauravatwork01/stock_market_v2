from flask import Blueprint, request
from app.services import MainAppService




app_bp = Blueprint("app", __name__, url_prefix="/app")


@app_bp.route("/get_hists", endpoint='get_hists', methods=["POST"])
def get_historicals():
    payload = request.get_json(silent=True) or {}

    service = MainAppService()
    data = service.get_historicals(payload)

    response = {
        "data" : data ,
        "status" : "done"
    }
    return response, 200





@app_bp.route("/sync_hists", endpoint='sync_hists', methods=["POST"])
def sync_historicals():
    payload = request.get_json(silent=True) or {}

    service = MainAppService()
    data = service.sync_historicals(payload)

    response = {
        "data" : data ,
        "status" : "done"
    }
    return response, 200





@app_bp.route("/todays_ohlc", endpoint='todays_ohlc', methods=["GET"])
def sync_historicals():
    # payload = request.get_json(silent=True) or {}

    service = MainAppService()
    data = service.get_todays_data()

    response = {
        "data" : data ,
        "status" : "done"
    }
    return response, 200




