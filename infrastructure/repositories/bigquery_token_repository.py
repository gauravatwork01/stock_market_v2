
from datetime import date, timedelta
from utilities import utilities
# from domains.vendor_auth.models import Token
from domains.broker_auth.models import Token

from infrastructure.api_clients.big_query_client import bigquery,\
get_bigquery_client, get_tokens_table_path




class BigQueryTokenRepository:

    def __init__(self, bigquery_client, token_table_path) -> None:
        self.client = bigquery_client
        self.token_table_path = token_table_path

    def create_token(self, token : Token):
        query = f"""
            INSERT INTO `{self.token_table_path}` 
            (token_date, access_token, request_token, updated_at, token_expiry)
            VALUES (@date, @access_token, @request_token, @updated_at, @token_expiry)
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("date", "DATE", token.token_date),
                bigquery.ScalarQueryParameter("access_token", "STRING", token.access_token),
                bigquery.ScalarQueryParameter("request_token", "STRING", token.request_token),
                bigquery.ScalarQueryParameter("updated_at", "TIMESTAMP", token.utc_updated_at),
                bigquery.ScalarQueryParameter("token_expiry", "TIMESTAMP", token.utc_token_expiry),
            ]
        )

        tokens = self.client.query(query, job_config=job_config).result()

    

    def update_token(self,token : Token):
        query = f"""
            UPDATE `{self.token_table_path}`
            SET
            access_token = @access_token,
            request_token = @request_token,
            updated_at = @updated_at,
            token_expiry = @token_expiry
            WHERE token_date = @token_date
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("token_date", "DATE", token.token_date),
                bigquery.ScalarQueryParameter("access_token", "STRING", token.access_token),
                bigquery.ScalarQueryParameter("request_token", "STRING", token.request_token),
                bigquery.ScalarQueryParameter("updated_at", "TIMESTAMP", token.utc_updated_at),
                bigquery.ScalarQueryParameter("token_expiry", "TIMESTAMP", token.utc_token_expiry),
            ]
        )

        resp = self.client.query(query, job_config=job_config).result()
        return resp


    def get_token_by_date(self, utc_target_date : date):
        query = f"""
            SELECT token_date, access_token, request_token, updated_at, token_expiry
            FROM `{self.token_table_path}`
            WHERE token_date = @filter_date
            LIMIT 1
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("filter_date", "DATE", utc_target_date)
            ]
        )
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()

        rows = list(results)
        if not rows:
            return None

        row = rows[0]

        return Token(
            token_date=row["token_date"],
            access_token=row["access_token"],
            request_token=row["request_token"],
            utc_updated_at=row["updated_at"],
            utc_token_expiry = row["token_expiry"]
        )


    def get_latest_token(self)->Token:
        query = f"""
            SELECT token_date, access_token, request_token, updated_at, token_expiry
            FROM `{self.token_table_path}`
            ORDER BY token_date DESC
            LIMIT 1
        """
        query_job = self.client.query(query)
        results = query_job.result() 

        rows = list(results)
        if not rows:
            return None

        row = rows[0]

        return Token(
            token_date= row["token_date"],
            access_token= row["access_token"],
            request_token= row["request_token"],
            utc_updated_at= row["updated_at"],
            utc_token_expiry= row["token_expiry"]
        ) 

