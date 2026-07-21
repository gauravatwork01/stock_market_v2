



from .gcp.bigquery_client import BigQueryClient
from .market_api_clients.kc_api_client import kc_api_client


__all__ = ["BigQueryClient", "kc_api_client"]



kc_client = None 

def get_kc_api_client():
    global kc_client
    if kc_client is None:
        kc_client = kc_api_client()
    return kc_client


bq_client = None 
def get_big_query_client():
    global bq_client
    if bq_client is None:
        bq_client = BigQueryClient()
    return bq_client
    


