from shared.infrastructure import get_big_query_client
from .bq_schema import TABLE_SCHEMA
from ..models.instrument import Instrument

class InstrumentRepository:


    def get_instruments(self):

        bq_client = get_big_query_client()
        query = f"""
            SELECT instr_token, symbol, name, exchange, created_at, updated_at
            FROM `{bq_client.project_id}.datawarehouse.{TABLE_SCHEMA['table_name']}`
        """
        results = bq_client.execute_query(
            query= query
        )
        
        instrument_models = []
        for each_res in results:
            instr = Instrument(
                instr_token = each_res["instr_token"],
                symbol = each_res["symbol"],
                name = each_res["name"],
                exchange = each_res["exchange"],
            )
            instrument_models.append(instr)

        return instrument_models






