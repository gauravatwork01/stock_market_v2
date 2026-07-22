
from contexts.broker_auth.application.services import get_access_token
from shared.infrastructure import get_kc_api_client
from datetime import datetime
from zoneinfo import ZoneInfo
from ..infra.kc_provider import KiteConnectProvider
import domain_services

class HistoricalAppService:



    def get_historicals(
        self,
        instr_token, 
        from_dt : datetime, 
        to_dt : datetime,
        interval : str 
    ):
        hists = domain_services.get_historicals(instr_token, from_dt, to_dt, interval)
        f_hists = [hist.model_dump(mode="json") for hist in hists] 
        return f_hists


    def sync_historicals(
        self,
        instr_token, 
        from_dt : datetime, 
        to_dt : datetime,
        interval : str 
    ):
        hists = domain_services.get_historicals(instr_token, from_dt, to_dt, interval)


