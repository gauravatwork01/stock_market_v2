
from shared.infrastructure import BigQueryClient
from pydantic import BaseModel
from google.cloud import bigquery


PY_TO_BQ_TYPE = {
    str: "STRING",
    int: "INTEGER",
    float: "FLOAT",
    bool: "BOOLEAN",
    dict: "JSON",
}

class FinancialsDB(BaseModel):  
    symbol: str
    quarter: int
    year: int
    data: dict
    source: str

    @classmethod
    def to_bq_schema(cls):
        bq_schema = []
        for name, field in cls.model_fields.items():
            bq_type = PY_TO_BQ_TYPE.get(field.annotation, "STRING")
            schema_field = bigquery.SchemaField(name, bq_type)
            bq_schema.append(schema_field)
        return bq_schema


class FinancialsRepo:
    def __init__(self):
        self.big_query_client = BigQueryClient()

    def upload_financials(self, financials_db:FinancialsDB):
        # Implement the logic to upload financial data to BigQuery

        merge_query = """
            MERGE `your_project.your_dataset.financials` AS target
            USING (
            SELECT
                '{symbol}' AS symbol,
                '{quarter}' AS quarter,
                {year} AS year,
                JSON '{data}' AS data,   -- adjust type if not JSON
                '{source}' AS source
            ) AS new_data
            ON  target.symbol = new_data.symbol
            AND target.quarter = new_data.quarter
            AND target.year = new_data.year
            WHEN NOT MATCHED THEN
            INSERT (symbol, quarter, year, data, source)
            VALUES (new_data.symbol, new_data.quarter, new_data.year, new_data.data, new_data.source)
        """
        table_details = {
            "name" : "financials", 
            "bq_schema" : FinancialsDB.to_bq_schema(),
            "partition_field" : None,
            "clustering_fields" : []
        }

        self.big_query_client.upsert_data_using_merge(
            table_dets = table_details,
            merge_query = merge_query,
            rows = [financials_db.dict()]
        )












