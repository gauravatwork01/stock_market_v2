


# from domains.instruments.models import Instrument
from contexts.instruments.domain.entities.instrument import Instrument
from contexts.instruments.domain.providers.instrument_data_provider import InstrumentDataProvider

class FinEdgeInstrumentProvider(InstrumentDataProvider):
    
    def __init__(self, finedge_client):
        self.finedge_client = finedge_client

    def fetch_instruments(self, exchange):
        raw_data = self.finedge_client.instruments(exchange = exchange)

        return [
            Instrument(
                symbol=i["tradingsymbol"],
                name=i["name"],
                exchange=i["exchange"],
                sector=None  # will be enriched later
            )
            for i in raw_data
        ]

