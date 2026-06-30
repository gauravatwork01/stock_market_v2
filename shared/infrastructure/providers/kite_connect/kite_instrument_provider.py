
from domains.instruments.models import Instrument


class KiteInstrumentProvider:
    
    def __init__(self, kite_client):
        self.kite_client = kite_client

    def fetch_instruments(self, exchange):
        raw_data = self.kite_client.instruments(exchange = exchange)

        return [
            Instrument(
                symbol=i["tradingsymbol"],
                name=i["name"],
                exchange=i["exchange"],
                sector=None  # will be enriched later
            )
            for i in raw_data
        ]

