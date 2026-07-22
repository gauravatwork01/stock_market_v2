from shared.infrastructure import get_big_query_client
from .bq_schema import TABLE_SCHEMA
from ..models.instrument import Instrument

class InstrumentRepository:

    def __init__(self) -> None:
        self.bq_client = get_big_query_client()


    def _format_results(self,results):
        models_by_id = {}
        for each_res in results:
            instr = Instrument(
                instr_token=each_res["instr_token"],
                symbol=each_res["symbol"],
                name=each_res["name"],
                exchange=each_res["exchange"],
            )
            models_by_id[instr.instr_token] = instr
        return models_by_id 


    def get_instruments_by_id(self, instr_ids: list):
        ids_csv = ",".join(str(i) for i in instr_ids)
        query = f"""
            SELECT instr_token, symbol, name, exchange, created_at, updated_at
            FROM `{self.bq_client.project_id}.datawarehouse.{TABLE_SCHEMA['table_name']}`
            WHERE instr_token IN ({ids_csv})
        """
        results = self.bq_client.execute_query(query=query)
        results_by_id = self._format_results(results)
        return results_by_id


    def get_instruments(self):
        query = f"""
            SELECT instr_token, symbol, name, exchange, created_at, updated_at
            FROM `{self.bq_client.project_id}.datawarehouse.{TABLE_SCHEMA['table_name']}`
        """
        results = self.bq_client.execute_query(
            query= query
        )
        results_by_id = self._format_results(results)
        return results_by_id






