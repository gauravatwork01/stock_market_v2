
from infrastructure.repositories.bigquery_holdings_repository import BigQueryHoldingsRepository
from domains.holdings.models import Holding
from infrastructure.providers.kite_connect.kite_holdings_provider import KiteHoldingsProvider


class KiteAuthUseCase:

    def __init__(self,kite_client, token_repo) -> None:
        self.kite_client = kite_client
        self.token_repo = token_repo

    def authenticate(self):
        latest_token = self.token_repo.get_latest_token()
        pass 





















