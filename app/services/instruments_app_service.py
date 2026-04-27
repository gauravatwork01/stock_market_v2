
from infrastructure.repositories.instruments_repository import (
    BQ_InstrumentsRepository,
    KC_InstrumentsRepository,
)


class InstrumentsApplicationService:


    def get_all_stocks():
        all_stocks = BQ_InstrumentsRepository.get_all_stocks()
        if len(all_stocks) == 0:
            all_stocks = KC_InstrumentsRepository.get_all_stocks()
        
        return all_stocks




















