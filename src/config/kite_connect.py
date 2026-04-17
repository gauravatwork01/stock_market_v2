

import logging
import os
from datetime import datetime, timezone
from services.datetime import DatetimeHelper
from kiteconnect import KiteConnect
from google.cloud import bigquery

logger = logging.getLogger(__name__)

API_KEY = "qjj8i06fi5r3s8ru"
API_SECRET = "hxqjy14n6rvk6vkqcllefhlabkbv13yx"

# kite_connect_client = 

class KiteConnectClient:

    def __init__(self) -> None:
        self.client = KiteConnect(api_key = API_KEY )

    def get_login_url(self):
        login_url = self.client.login_url()
        return login_url

    def get_access_token(self,request_token):
        access_token = self.client.generate_session(request_token, api_secret=API_SECRET)
        return access_token



class KiteConnectVendor:
    def __init__(self) -> None:
        self._bq_client = bigquery.Client() 


    # def 

    def save_request_token(self, req_token: str) -> None:

        row = {
            "user_id" : "default-gaurav",
            "request_token": req_token,
            "timestamp": DatetimeHelper.now_ist().isoformat(),
        }
        table_ref = self._bq_client.dataset("datawarehouse").table("request_tokens")
        errors = self._bq_client.insert_rows_json(
            table= table_ref, 
            json_rows = [row]
        )
        if errors:
            raise RuntimeError(f"BigQuery insert_rows_json failed: {errors}")

        return errors









