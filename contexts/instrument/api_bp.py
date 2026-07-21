from flask import Blueprint, redirect, request, render_template 
from .application.services import InstrumentService 
from .models.instrument import Instrument


instrument_bp = Blueprint("instrument", __name__, url_prefix="/instrument")


@instrument_bp.route("/sync", endpoint='sync')
def sync_instruments():
    instr_service = InstrumentService()
    instruments = instr_service.sync_instruments()
    return {"status":"done"}, 200


@instrument_bp.route("/get", endpoint="get")
def get_instruments():
    instr_service = InstrumentService()
    instruments: list[Instrument] = instr_service.get_instruments()
    response_data = [instr.model_dump() for instr in instruments]
    return {"data":response_data}, 200
    
























