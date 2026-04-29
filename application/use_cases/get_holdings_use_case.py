

from typing import List

# from domain.holding import Holding
# from domain.repositories.holding_repository import HoldingRepository
from infrastructure.repositories.bigquery_holdings_repository import BigQueryHoldingsRepository
from domains.holdings.models import Holding
from infrastructure.providers.kite_connect.kite_holdings_provider import KiteHoldingsProvider
class GetHoldingsUseCase:
    """
    Use case:
    - Try to get holdings from repository (fast path)
    - If not present (or stale), fetch from provider
    - Persist and return
    """

    def __init__(
        self,
        holdings_repo: BigQueryHoldingsRepository,
        kite_provider: KiteHoldingsProvider,  
    ):
        self.holdings_repo = holdings_repo
        self.kite_provider = kite_provider


    def get_holdings(self):
        holdings = self.holdings_repo.get_all_holdings()
        if not holdings:
            holdings = self.kite_provider.get_all_holdings()
        return holdings



