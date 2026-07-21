from shared.infrastructure import get_kc_api_client, get_big_query_client
from contexts.broker_auth.application.services import get_access_token
from utilities import utilities
from ..infrastructure.bq_schema import SCHEMA
from ..infrastructure.instrument_repo import InstrumentRepository
from ..models import Instrument


class InstrumentService:



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



    def get_instruments(self):
        instr_repo = InstrumentRepository()
        instruments: list[Instrument] = instr_repo.get_instruments()
        return instruments 