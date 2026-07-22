from flask import Blueprint, request
from app.services import MainAppService




app_bp = Blueprint("app", __name__, url_prefix="/app")


@app_bp.route("/get_hists", endpoint='get_hists', methods=["POST"])
def get_historicals():
    payload = request.get_json(silent=True) or {}

    service = MainAppService(payload)
    data = service.get_historicals()

    response = {
        "data" : data ,
        "status" : "done"
    }
    return response, 200
