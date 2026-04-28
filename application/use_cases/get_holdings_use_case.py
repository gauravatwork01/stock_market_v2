

from typing import List

# from domain.holding import Holding
# from domain.repositories.holding_repository import HoldingRepository
from infrastructure.repositories.

class GetHoldingsUseCase:
    """
    Use case:
    - Try to get holdings from repository (fast path)
    - If not present (or stale), fetch from provider
    - Persist and return
    """

    def __init__(
        self,
        holding_repo: HoldingRepository,
        kite_provider,  # ideally type: PortfolioProvider / HoldingsProvider
    ):
        self.holding_repo = holding_repo
        self.kite_provider = kite_provider

    def execute(self, force_refresh: bool = False) -> List[Holding]:
        # 1. Try repo
        if not force_refresh:
            holdings = self.holding_repo.get_all()
            if holdings:
                return holdings

        # 2. Fetch from provider
        portfolio = self.kite_provider.fetch_portfolio()
        holdings = portfolio.holdings

        # 3. Persist
        if holdings:
            self.holding_repo.save_all(holdings)

        return holdings



