
from datetime import date, timedelta
from utilities import utilities
# from domains.vendor_auth.models import Token
# from domains.broker_auth.models import Token
from contexts.broker_auth.models import Token

from shared.infrastructure.gcp.bigquery_client import BigQueryClient




class BigQueryTokenRepository:

    def __init__(self, bigquery_client: BigQueryClient) -> None:
        self.client = bigquery_client
        self.token_table_path = f"{bigquery_client.project}.datawarehouse.tokens"

    def create_token(self, token : Token):
        query = f"""
            INSERT INTO `{self.token_table_path}` 
            (ist_expiry_dt, request_token, access_token, updated_at_ts)
            VALUES (@ist_expiry_dt, @request_token, @access_token, @updated_at_ts)
        """
        query_params = [
            ["ist_expiry_dt", "DATETIME", token.ist_expiry_dt],
            ["request_token", "STRING", token.request_token],
            ["access_token", "STRING", token.access_token],
            ["updated_at_ts", "TIMESTAMP", token.updated_at_ts],
        ]
        query_resp = self.client.execute_query(
            query = query,
            query_params = query_params
        )

    

    def update_token(self,token : Token):
        query = f"""
            UPDATE `{self.token_table_path}`
            SET
            request_token = @request_token,
            access_token = @access_token,
            updated_at_ts = @updated_at_ts
            WHERE ist_expiry_dt = @ist_expiry_dt
        """
        query_params = [
            ["request_token", "STRING", token.request_token],
            ["access_token", "STRING", token.access_token],
            ["updated_at_ts", "TIMESTAMP", token.updated_at_ts],
            ["ist_expiry_dt", "DATETIME", token.ist_expiry_dt],
        ]
        query_resp = self.client.execute_query(
            query = query,
            query_params = query_params
        )
        return query_resp

    def get_token_by_expiry_datetime(self, ist_datetime):
        query = f"""
            SELECT ist_expiry_dt, request_token, access_token, updated_at_ts
            FROM `{self.token_table_path}`
            WHERE ist_expiry_dt = @ist_expiry_dt
            LIMIT 1
        """
        query_params = [
            ["ist_expiry_dt", "DATETIME", ist_datetime]
        ]
        query_resp = self.client.execute_query(
            query = query,
            query_params = query_params
        )
        rows = list(query_resp)
        if not rows:
            return None

        row = rows[0]

        return Token(
            ist_expiry_dt = row["ist_expiry_dt"],
            request_token = row["request_token"],
            access_token = row["access_token"],
            updated_at_ts=row["updated_at_ts"]
        )
        


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
            token_date = row["token_date"],
            access_token = row["access_token"],
            request_token = row["request_token"],
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

