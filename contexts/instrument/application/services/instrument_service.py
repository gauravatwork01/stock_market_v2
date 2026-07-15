

# the application service 
# orchestrates use-cases using domain abstractions
from typing import List
from contexts.instrument.models import Instrument
from contexts.instrument.domain.providers.instrument_data_provider import InstrumentDataProvider

class InstrumentService:

    def __init__(self, provider: InstrumentDataProvider):
        self.provider = provider

    def fetch_instruments(self, exchange: str) -> List[Instrument]:
        return self.provider.fetch_instruments(exchange)





