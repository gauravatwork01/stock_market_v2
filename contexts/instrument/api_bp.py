from flask import Blueprint, redirect, request, render_template 
from .services.app_services import InstrumentAppService
from .models.instrument import Instrument


instrument_bp = Blueprint("instrument", __name__, url_prefix="/instrument")


@instrument_bp.route("/sync", endpoint='sync')
def sync_instruments():
    instr_service = InstrumentAppService()
    instruments = instr_service.sync_instruments()
    return {"status":"done"}, 200


@instrument_bp.route("/get", endpoint="get")
def get_instruments():
    instr_service = InstrumentAppService()
    instruments: list[Instrument] = instr_service.get_company_stocks()

    response = {
        "count" : len(instruments),
        "data" : instruments
    }
    return response, 200
    
























