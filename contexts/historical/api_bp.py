
from .services.app_services import HistoricalAppService
from flask import Blueprint, redirect, request, render_template 
from contexts.broker_auth.application.services import kite_authentication_required


historical_bp = Blueprint("historical", __name__, url_prefix="/historical")




@historical_bp.route("/get", endpoint='get')
def get_historicals():    
    data = HistoricalAppService().get_historicals()
    return render_template("portfolio.html", holdings=[])


@historical_bp.route("/sync", endpoint='sync', methods=["POST"])
def sync_historicals():    
    payload = request.get_json()

    instr_token = payload.get("instr_token")
    from_dt = payload.get("from_dt")
    to_dt = payload.get("to_dt")
    interval = payload.get("interval")

    app_service = HistoricalAppService()
    app_service.sync_historicals(
        instr_token = instr_token,
        from_dt = from_dt,
        to_dt = to_dt,
        interval = interval
    )
    return {"status":"done"}, 200 






















