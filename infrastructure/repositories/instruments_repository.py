


from app.services.instruments_repository_interface import InstrumentsRepository
from infrastructure.api_clients.kite_connect_client import KiteConnectAPIClient
from infrastructure.api_clients.big_query_client import get_bigquery_client


# class StorageInstrumentsRepo:
# class NSEInstrumentsRepo:
# class KiteInstrumentsRepo:






# kite-connect
class KC_InstrumentsRepository(InstrumentsRepository):

    @staticmethod 
    def get_all_stocks():
        kc_api_client = KiteConnectAPIClient()
        all_stocks = kc_api_client.instruments.get_all_stocks()
        return all_stocks 




# big-query
class BQ_InstrumentsRepository(InstrumentsRepository):

    @staticmethod 
    def get_all_stocks():
        bq_api_client = get_bigquery_client()
        return []






