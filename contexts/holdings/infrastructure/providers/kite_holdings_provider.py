# from domains.portfolio.models import  Holding
from domains.holdings.models import Holding


class KiteHoldingsProvider:
    def __init__(self, kite_client):
        self.kite_client = kite_client

    def get_all_holdings(self) -> Holding:
        kite_holdings = self.kite_client.holdings()

        holdings = []
        for each_kite_holding in kite_holdings:
            holding = Holding(
                symbol= each_kite_holding["tradingsymbol"],
                quantity= each_kite_holding["quantity"],
                avg_acquisition_price= each_kite_holding["average_price"],
                recent_trade_price= each_kite_holding["last_price"],
                yesterdays_close_price= each_kite_holding["close_price"],
            )
            holdings.append(holding)

        return holdings


