from shared.infrastructure import BigQueryClient
from .hist_schema import HIST_SCHEMA
import uuid
from ...models import Historical
from utilities.utilities import log_time


class HistoricalRepository:

    TABLE_NAME = "historical"

    def __init__(self) -> None:
        self.bq_client = BigQueryClient()


    def get_merge_query(self) -> str:
        merge_query = """
            MERGE `{main_tbl_id}` M
            USING `{staging_tbl_id}` S
            ON M.instr_token = S.instr_token
               AND M.`interval` = S.`interval`
               AND M.datetime = S.datetime
            WHEN MATCHED THEN UPDATE SET
                symbol = S.symbol,
                open = S.open,
                high = S.high,
                low = S.low,
                close = S.close
            WHEN NOT MATCHED THEN INSERT
                (instr_token, symbol, `interval`, open, high, low, close, datetime)
                VALUES
                (S.instr_token, S.symbol, S.`interval`, S.open, S.high, S.low, S.close, S.datetime)
        """
        return merge_query

    def sync_values(self, hists: list[Historical]):

        table_details = {
            "name" : self.TABLE_NAME, 
            "bq_schema" : HIST_SCHEMA,
            "partition_field" : "datetime",
            "clustering_fields" : ["interval"]
        }
        merge_query = self.get_merge_query()
        raw_hists = [hist.model_dump(context={"include_only_table_columns": True}, mode="json") for hist in hists] 
        self.bq_client.upsert_data_using_merge(
            table_dets = table_details,
            merge_query = merge_query,
            rows = raw_hists
        )



