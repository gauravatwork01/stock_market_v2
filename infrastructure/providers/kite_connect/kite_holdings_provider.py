# from domains.portfolio.models import  Holding
from domains.holdings.models import Holding


class KiteHoldingsProvider:
    def __init__(self, kite_client):
        self.kite_client = kite_client

    def get_all_holdings(self) -> Holding:
        kite_holdings = self.kite_client.holdings()

        holdings = [
            Holding(
                symbol= each_kite_holding["tradingsymbol"],
                quantity = each_kite_holding["quantity"],
                avg_price= each_kite_holding["average_price"]
            )
            for each_kite_holding in kite_holdings
        ]

        return holdings


