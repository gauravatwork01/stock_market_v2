from domains.portfolio.models import  Holding


class KiteHoldingProvider:
    def __init__(self, kite_client):
        self.kite_client = kite_client

    def fetch_portfolio(self) -> Holding:
        raw = self.kite_client.holdings()

        holdings = [
            Holding(
                symbol=i["tradingsymbol"],
                quantity=i["quantity"],
                avg_price=i["average_price"]
            )
            for i in raw
        ]

        return holdings


