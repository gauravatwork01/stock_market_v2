
from src.config.bigquery import bigquery, bigquery_client, TOKENS_TABLE_PATH
from datetime import date
from src.broker.kite_connect.auth.models import Token


class TokenRepository:

    def create_update_token(self, request_token, access_token, target_date : date):
        existing_token = self.token_exists_for_date(target_date= target_date)
        if existing_token:
            resp = self.update_token_for_date(
                request_token= request_token,
                access_token= access_token,
                target_date= target_date
            ) 
            msg = "Updated"
        else:
            resp = self.create_token_for_date(
                request_token= request_token,
                access_token= access_token,
                target_date= target_date
            )
            msg = "Created"
        
        return (resp, msg)

    def create_token_for_date(self, request_token, access_token, target_date : date):
        query = f"""
            INSERT INTO `{TOKENS_TABLE_PATH}` (token_date, access_token, request_token)
            VALUES (@date, @access_token, @request_token)
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("date", "DATE", target_date),
                bigquery.ScalarQueryParameter("access_token", "STRING", access_token),
                bigquery.ScalarQueryParameter("request_token", "STRING", request_token),
            ]
        )

        tokens = bigquery_client.query(query, job_config=job_config).result()
        return tokens[0]
    
    def update_token_for_date(self,request_token, access_token, target_date : date):
        query = f"""
            UPDATE `{TOKENS_TABLE_PATH}`
            SET
            access_token = @access_token,
            request_token = @request_token
            WHERE token_date = @date
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("date", "DATE", target_date),
                bigquery.ScalarQueryParameter("access_token", "STRING", access_token),
                bigquery.ScalarQueryParameter("request_token", "STRING", request_token),
            ]
        )

        resp = bigquery_client.query(query, job_config=job_config).result()
        return resp


    def token_exists_for_date(self, target_date : date):
        query = f"""
            SELECT token_date, access_token, request_token
            FROM `{TOKENS_TABLE_PATH}`
            WHERE token_date = @filter_date
            LIMIT 1
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("filter_date", "DATE", target_date)
            ]
        )
        query_job = bigquery_client.query(query, job_config=job_config)
        results = query_job.result()

        rows = list(results)
        if not rows:
            return None

        row = rows[0]

        return Token(
            token_date=row["token_date"],
            access_token=row["access_token"],
            request_token=row["request_token"],
        ) 




