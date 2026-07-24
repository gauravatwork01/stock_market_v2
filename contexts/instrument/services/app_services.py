from shared.infrastructure import get_kc_api_client, get_big_query_client
from contexts.broker_auth.application.services import get_access_token
from utilities import utilities
from ..infrastructure.bq_schema import SCHEMA
from ..infrastructure.instrument_repo import InstrumentRepository
from ..models import Instrument
from . import domain_services


class InstrumentAppService:



    def sync_instruments(self):
        kc_api_clt = get_kc_api_client()
        acces_token = get_access_token()
        kc_api_clt.set_access_token(acces_token)
        instruments = kc_api_clt.get_instruments_by_exchange(exchange = "NSE")

        now_ist = utilities.get_ist_now_datetime().isoformat(sep=" ")
        for each_instr in instruments:
            each_instr["created_at"] = now_ist
            each_instr["updated_at"] = now_ist

        bq_client = get_big_query_client()
        bq_client.upsert_data_using_merge(
            schema = SCHEMA,
            rows = instruments,
            table_name = "instrument"
        )

        return True 



    def get_all_instruments(self):
        instr_repo = InstrumentRepository()
        instruments_by_id: dict[str,Instrument] = instr_repo.get_instruments()
        return instruments_by_id 

    

    def get_company_stocks(self):
        instr_repo = InstrumentRepository()
        instruments_by_id: dict[str,Instrument] = instr_repo.get_instruments()
        comp_stocks = domain_services.filter_company_stocks(instruments_by_id)
        comp_stocks = [stock.model_dump() for stock in comp_stocks]
        return comp_stocks




    def get_instruments_by_id(self, instr_ids:list):
        instr_repo = InstrumentRepository()
        instruments_by_id: dict[str,Instrument] = instr_repo.get_instruments_by_id(instr_ids = instr_ids)
        for instr_id, instr_model in instruments_by_id.items():
            instruments_by_id[instr_id] = instr_model.model_dump()
        return instruments_by_id

