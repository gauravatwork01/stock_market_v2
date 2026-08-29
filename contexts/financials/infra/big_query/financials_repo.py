
from shared.infrastructure import BigQueryClient
from pydantic import BaseModel
from google.cloud import bigquery
from contexts.financials.models import FinancialReport 


# PY_TO_BQ_TYPE = {
#     str: "STRING",
#     int: "INTEGER",
#     float: "FLOAT",
#     bool: "BOOLEAN",
#     dict: "JSON",
# }
SCHEMA = [
    bigquery.SchemaField("isin", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("symbol", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("source", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("quarter", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("year", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("report_nature", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("data", "JSON", mode="REQUIRED"),
    bigquery.SchemaField("source_link", "STRING", mode="NULLABLE"),
]
# class FinancialsRow(BaseModel):  
#     symbol: str
#     quarter: str
#     year: int
#     data: dict
#     source: str

#     @classmethod
#     def to_bq_schema(cls):
#         bq_schema = []
#         for name, field in cls.model_fields.items():
#             bq_type = PY_TO_BQ_TYPE.get(field.annotation, "STRING")
#             schema_field = bigquery.SchemaField(name, bq_type)
#             bq_schema.append(schema_field)
#         return bq_schema


class FinancialsRepo:
    def __init__(self):
        self.big_query_client = BigQueryClient()


    def get_row_json(self, financial_report:FinancialReport):  
        data_row =  {
            "symbol": financial_report.symbol,
            "quarter": financial_report.quarter,
            "year": financial_report.fin_year,
            "data": financial_report.dict(),
            "source": financial_report.source,
            "report_nature" : financial_report.nature_of_report,
            "source_link": financial_report.source_link,
            "isin": financial_report.isin
        }
        return data_row


    def upload_financials(self, financial_report:FinancialReport):

        data_row = self.get_row_json(financial_report)
        
        merge_query = """
            MERGE `{main_tbl_id}` M
            USING `{staging_tbl_id}` S
            ON M.source = S.source
                AND M.report_nature = S.report_nature
                AND M.isin = S.isin
                AND M.year = S.year
                AND M.quarter = S.quarter
            WHEN MATCHED THEN UPDATE SET
                data = S.data,
                source_link = S.source_link,
                isin = S.isin
            WHEN NOT MATCHED THEN INSERT
                (symbol, quarter, year, data, source, report_nature, source_link, isin)
                VALUES
                (S.symbol, S.quarter, S.year, S.data, S.source, S.report_nature, S.source_link, S.isin)
        """
        table_details = {
            "name" : "financials", 
            "bq_schema" : SCHEMA,
            "partition_field" : None,
            "clustering_fields" : []
        }

        self.big_query_client.upsert_data_using_merge(
            table_dets = table_details,
            merge_query = merge_query,
            rows = [data_row]
        )
        print(f"Uploaded {financial_report.symbol}: {financial_report.quarter}-{financial_report.fin_year}, {financial_report.nature_of_report}")







    def get_financials(self, isin):
        QUERY = """
            SELECT *
            FROM `stock-market-452020.datawarehouse.financials`
            WHERE isin = '{isin}'
        """

        QUERY = QUERY.format(isin=isin)
        results = self.big_query_client.execute_query(QUERY)

        financial_reports = []
        for row in results:
            financial_reports.append(FinancialReport(**row.get("data")))
            # financial_reports.append(row.get("data"))

        return financial_reports




