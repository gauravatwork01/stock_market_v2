



from .gcp.bigquery_client import BigQueryClient
from .market_api_clients.kc_api_client import kc_api_client
from ..infrastructure.gcp.task_queue_client import TaskQueueClient 


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
    


task_queue_client = None 
def get_task_queue_client():
    global task_queue_client
    if task_queue_client is None:
        task_queue_client = TaskQueueClient()

    return task_queue_client