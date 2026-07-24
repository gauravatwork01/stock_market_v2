from shared.infrastructure import get_kc_api_client
from contexts.broker_auth.application.services import get_access_token
from datetime import datetime
from dateutil import parser as dateutil_parser
from zoneinfo import ZoneInfo
from contexts.instrument.services.app_services import InstrumentAppService
from contexts.historical.services.app_services import HistoricalAppService
from utilities.utilities import log_time

class MainAppService:
  

    def _parse_ist_datetime(self, value: str) -> datetime:
        dt = dateutil_parser.parse(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
        return dt


    def get_historicals(self, payload):
        instr_token = payload.get("instr_token")
        from_dt = payload.get("from_dt")
        to_dt = payload.get("to_dt")
        interval = payload.get("interval")

        instr_app_service = InstrumentAppService()
        instruments_by_id = instr_app_service.get_instruments_by_id(
            instr_ids = [instr_token]
        )
        instrument_dets = instruments_by_id[instr_token]

        hist_app_service = HistoricalAppService()
        hists = hist_app_service.get_historicals(
            instr_token= instr_token,
            from_dt = self._parse_ist_datetime(from_dt),
            to_dt = self._parse_ist_datetime(to_dt),
            interval = interval
        )
        data = {
            "instr_details" : instrument_dets,
            "historicals" : hists 
        }
        return data  

    @log_time
    def sync_historicals(self, payload):
        instr_token = payload.get("instr_token")
        from_dt = payload.get("from_dt")
        to_dt = payload.get("to_dt")
        interval = payload.get("interval")

        instr_app_service = InstrumentAppService()
        instruments_by_id = instr_app_service.get_instruments_by_id(
            instr_ids = [instr_token]
        )
        instrument_dets = instruments_by_id[instr_token]

        hist_app_service = HistoricalAppService()
        hists = hist_app_service.sync_historicals(
            instr_token = instr_token,
            from_dt = self._parse_ist_datetime(from_dt),
            to_dt = self._parse_ist_datetime(to_dt),
            interval = interval
        )
        data = {
            "instr_details" : instrument_dets,
            "historicals" : hists 
        }
        return data  
        


    def get_todays_data(self):
        instr_app_service = InstrumentAppService()
        comp_stocks = instr_app_service.get_company_stocks()
        instr_ids = [each_instr["instr_token"] for each_instr in comp_stocks]
        instr_id_batches = []

        batch_size = 1000
        for i in range(0,len(instr_ids), batch_size):
            instr_id_batch = instr_ids[i:i+batch_size]
            instr_id_batches.append(instr_id_batch)
             

        hist_app_service = HistoricalAppService()
        hist_app_service.get_todays_data(instr_id_batches[0])
        pass 




from flask import url_for
from shared.infrastructure import get_task_queue_client
class MainSyncService:

    @log_time
    def sync_all_historicals(self, payload):
        from_dt = payload.get("from_dt")
        to_dt = payload.get("to_dt")
        interval = payload.get("interval")

        instr_app_service = InstrumentAppService()
        instruments_by_id = instr_app_service.get_all_instruments()

        instr_ids = list(instruments_by_id.keys())[0:4]

        task_queue_client = get_task_queue_client()
        for instr_id in instr_ids:
            payload = {
                "from_dt" : from_dt,
                "to_dt" : to_dt,
                "interval" : interval,
                "instr_token" : instr_id
            }
            task_queue_client.create_task_queue(
                payload = payload,
                endpoint = url_for("app.sync_historicals")
            )
        
        
        return True 