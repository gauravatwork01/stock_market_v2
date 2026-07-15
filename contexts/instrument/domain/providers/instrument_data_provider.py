# contexts/instruments/domain/providers/instrument_data_provider.py

from abc import ABC, abstractmethod
from typing import List

from contexts.instrument.models import Instrument


class InstrumentDataProvider(ABC):

    @abstractmethod
    def fetch_instruments(self, exchange: str) -> List[Instrument]:
        """
        Fetch all instruments for a given exchange.
        """
        pass

    