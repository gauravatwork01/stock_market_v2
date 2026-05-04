

# domains/holdings/domain/repositories/holdings_repository.py

from abc import ABC, abstractmethod

class HoldingsRepository(ABC):

    @abstractmethod
    def get_portfolio(self):
        pass

    @abstractmethod
    def save_position(self, position):
        pass

    @abstractmethod
    def update_position(self, position):
        pass
    