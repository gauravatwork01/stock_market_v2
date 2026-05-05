
# from domains.instruments.models import Instrument
from contexts.instrument.domain.entities.instrument import Instrument
from contexts.instrument.domain.providers.instrument_data_provider import InstrumentDataProvider

class KiteInstrumentProvider(InstrumentDataProvider):
    
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

