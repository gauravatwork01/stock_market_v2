
from src.config.bigquery import bigquery, get_bigquery_client, get_tokens_table_path
from datetime import date, timedelta
from src.broker.kite_connect.auth.models import Token
from utilities import utilities




def get_valid_token_date():
    ist_now = utilities.get_ist_datetime()
    token_date = ist_now.date()
    if ist_now.hour < 6:
        token_date = token_date - timedelta(days= 1)
    return token_date



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
            INSERT INTO `{get_tokens_table_path()}` 
            (token_date, access_token, request_token, updated_at, token_expiry)
            VALUES (@date, @access_token, @request_token, @updated_at, @token_expiry)
        """
        updated_at = utilities.get_ist_datetime()
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("date", "DATE", target_date),
                bigquery.ScalarQueryParameter("access_token", "STRING", access_token),
                bigquery.ScalarQueryParameter("request_token", "STRING", request_token),
                bigquery.ScalarQueryParameter("updated_at", "TIMESTAMP", updated_at),
                bigquery.ScalarQueryParameter("token_expiry", "TIMESTAMP", token_expiry_datetime),
            ]
        )

        tokens = get_bigquery_client().query(query, job_config=job_config).result()
        return tokens[0]
    
    def update_token_for_date(self,request_token, access_token, target_date : date):
        query = f"""
            UPDATE `{get_tokens_table_path()}`
            SET
            access_token = @access_token,
            request_token = @request_token,
            updated_at = @updated_at
            WHERE token_date = @date
        """
        updated_at = utilities.get_ist_datetime()
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("date", "DATE", target_date),
                bigquery.ScalarQueryParameter("access_token", "STRING", access_token),
                bigquery.ScalarQueryParameter("request_token", "STRING", request_token),
                bigquery.ScalarQueryParameter("updated_at", "TIMESTAMP", updated_at),
            ]
        )

        resp = get_bigquery_client().query(query, job_config=job_config).result()
        return resp


    def token_exists_for_date(self, target_date : date):
        query = f"""
            SELECT token_date, access_token, request_token, updated_at
            FROM `{get_tokens_table_path()}`
            WHERE token_date = @filter_date
            LIMIT 1
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("filter_date", "DATE", target_date)
            ]
        )
        query_job = get_bigquery_client().query(query, job_config=job_config)
        results = query_job.result()

        rows = list(results)
        if not rows:
            return None

        row = rows[0]

        return Token(
            token_date=row["token_date"],
            access_token=row["access_token"],
            request_token=row["request_token"],
            updated_at=row["updated_at"],
        )

    def get_token_for_date(self, target_date : date):
        query = f"""
            SELECT token_date, access_token, request_token, updated_at
            FROM `{get_tokens_table_path()}`
            WHERE token_date = @filter_date
            LIMIT 1
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("filter_date", "DATE", target_date)
            ]
        )
        query_job = get_bigquery_client().query(query, job_config=job_config)
        results = query_job.result()

        rows = list(results)
        if not rows:
            return None

        row = rows[0]

        return Token(
            token_date=row["token_date"],
            access_token=row["access_token"],
            request_token=row["request_token"],
            updated_at=row["updated_at"],
        ) 


    def get_todays_token(self):
        ist_now = utilities.get_ist_datetime()
        existing_token = self.token_exists_for_date(
            target_date= ist_now.date()
        )
        return existing_token 


    def get_latest_token(self)->Token:
        query = f"""
            SELECT token_date, access_token, request_token, updated_at, token_expiry
            FROM `{get_tokens_table_path()}`
            ORDER BY token_date DESC
            LIMIT 1
        """
        query_job = get_bigquery_client().query(query)
        results = query_job.result() 

        rows = list(results)
        if not rows:
            return None

        row = rows[0]

        return Token(
            token_date=row["token_date"],
            access_token=row["access_token"],
            request_token=row["request_token"],
            updated_at=row["updated_at"],
            token_expiry= row["token_expiry"]
        ) 

