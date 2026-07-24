from flask import Blueprint, request
from app.services import MainAppService, MainSyncService




app_bp = Blueprint("app", __name__, url_prefix="/app")


@app_bp.route("/historicals/get", endpoint='get_historicals', methods=["POST"])
def get_historicals():
    payload = request.get_json(silent=True) or {}

    service = MainAppService()
    data = service.get_historicals(payload)

    response = {
        "data" : data ,
        "status" : "done"
    }
    return response, 200





@app_bp.route("/historicals/sync", endpoint='sync_historicals', methods=["POST"])
def sync_historicals():
    payload = request.get_json(silent=True) or {}

    service = MainAppService()
    data = service.sync_historicals(payload)

    response = {
        "data" : data ,
        "status" : "done"
    }
    return response, 200


@app_bp.route("/historicals/sync-all", endpoint='sync_all_historicals', methods=["POST"])
def sync_all_historicals():
    payload = request.get_json()
    
    service = MainSyncService()
    data = service.sync_all_historicals(payload)

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




