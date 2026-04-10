
from google.cloud import bigquery


class BigQueryManager:
    client = bigquery.Client()
    dataset = "datawarehouse"

    @classmethod
    def get_table_path(cls,table_name):

        return f"{cls.client.project_id}.{cls.dataset}.{table_name}"




