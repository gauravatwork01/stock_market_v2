from domains.holdings.models import Holding
from typing import List



class BigQueryHoldingsRepository:

    def __init__(self, bigquery_client) -> None:
        self.client = bigquery_client


    def get_all_holdings(self) -> List[Holding]:
        query = f"""
            SELECT token_date, access_token, request_token, updated_at, token_expiry
            FROM `{get_tokens_table_path()}`
            ORDER BY token_date DESC
            LIMIT 1
        """
        pass 












