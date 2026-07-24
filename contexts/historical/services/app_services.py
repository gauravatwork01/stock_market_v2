
from contexts.broker_auth.application.services import get_access_token
from shared.infrastructure import get_kc_api_client
from datetime import datetime
from zoneinfo import ZoneInfo
from ..infra.kc_provider import KiteConnectProvider
from . import domain_services
from ..models import Historical
from ..infra.big_query.hist_repo import HistoricalRepository
from utilities.utilities import log_time

class HistoricalAppService:



    def get_historicals(
        self,
        instr_token, 
        from_dt : datetime, 
        to_dt : datetime,
        interval : str 
    ):
        hists: list[Historical] = domain_services.get_historicals(instr_token, from_dt, to_dt, interval)
        f_hists = [hist.model_dump(context={"exclude_calculations": True}, mode="json") for hist in hists] 
        return f_hists


    @log_time
    def sync_historicals(
        self,
        instr_token, 
        from_dt : datetime, 
        to_dt : datetime,
        interval : str 
    ):
        hists: list[Historical] = domain_services.get_historicals(instr_token, from_dt, to_dt, interval)
        hist_repo = HistoricalRepository()
        hist_repo.sync_values(hists)



    def get_todays_data(self, instr_ids):
        kc_provider = KiteConnectProvider()
        kc_provider.get_todays_ohlc(instr_ids)
        pass 

