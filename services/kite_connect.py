import logging
import os
from datetime import datetime, timezone
from services.datetime import DatetimeHelper

from google.cloud import bigquery

logger = logging.getLogger(__name__)

API_KEY = "qjj8i06fi5r3s8ru"
LOGIN_ENDPOINT = f"https://kite.zerodha.com/connect/login?v=3&api_key={API_KEY}"

# Set BIGQUERY_KITE_REQUEST_TOKEN_TABLE to "project.dataset.table".
# ADC (including GOOGLE_APPLICATION_CREDENTIALS → service account JSON) is used automatically.


class KiteConnect:
    def __init__(self) -> None:
        self._bq_client = bigquery.Client() 

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
