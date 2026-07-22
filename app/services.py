from shared.infrastructure import get_kc_api_client
from contexts.broker_auth.application.services import get_access_token
from datetime import datetime
from dateutil import parser as dateutil_parser
from zoneinfo import ZoneInfo
from contexts.instrument.application.services import InstrumentAppService
from contexts.historical.app.services import HistoricalAppService

class MainAppService:

    def __init__(self,payload) -> None:
        self.instr_token = payload.get("instr_token")
        self.from_dt = payload.get("from_dt")
        self.to_dt = payload.get("to_dt")
        self.interval = payload.get("interval")
        

    def _parse_ist_datetime(self, value: str) -> datetime:
        dt = dateutil_parser.parse(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
        return dt


    def get_historicals(self):

        instr_app_service = InstrumentAppService()
        instruments_by_id = instr_app_service.get_instruments_by_id(
            instr_ids = [self.instr_token]
        )
        instrument_dets = instruments_by_id[self.instr_token]

        hist_app_service = HistoricalAppService()
        hists = hist_app_service.get_historicals(
            instr_token= self.instr_token,
            from_dt = self._parse_ist_datetime(self.from_dt),
            to_dt = self._parse_ist_datetime(self.to_dt),
            interval = self.interval
        )
        data = {
            "instr_details" : instrument_dets,
            "historicals" : hists 
        }
        return data  
        
