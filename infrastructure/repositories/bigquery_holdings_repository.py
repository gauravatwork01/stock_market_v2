from domains.holdings.models import Holding
from typing import List



class BigQueryHoldingsRepository:

    def __init__(self, bigquery_client) -> None:
        self.client = bigquery_client


    def get_all_holdings(self) -> List[Holding]:
        return [] 












