
from abc import ABC, abstractmethod


class I_MarketApiClient(ABC):

    def get_all_holdings():
        ...

    def get_all_stocks():
        ... 

    @abstractmethod
    def get_instruments_by_exchange():
        ... 
