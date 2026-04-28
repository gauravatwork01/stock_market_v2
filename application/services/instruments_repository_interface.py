from abc import ABC, abstractmethod
from typing import List, Optional


class InstrumentsRepository(ABC):

    @abstractmethod
    def get_all_stocks(self):
        pass




