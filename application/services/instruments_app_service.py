
from infrastructure.repositories.instruments_repository import (
    BQ_InstrumentsRepository,
    KC_InstrumentsRepository,
)

class SyncInstrumentsUseCase:
    def __init__(self, repo, kite_provider, nse_csv_reader):
        self.repo = repo
        self.kite = kite_provider
        self.nse = nse_csv_reader

    def execute(self, csv_file):
        # 1. Fetch base instruments (Kite = source of instruments)
        instruments = self.kite.fetch_instruments()

        # 2. Get sector mapping (NSE CSV = source of sector truth)
        sector_map = self.nse.get_sector_map(csv_file)

        # 3. Enrich instruments
        for inst in instruments:
            inst.sector = sector_map.get(inst.symbol)

        # 4. Persist
        self.repo.save(instruments)


















