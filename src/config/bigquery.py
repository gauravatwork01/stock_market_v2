


from google.cloud import bigquery


# bigquery = bigquery
bigquery_client = None 

def get_bigquery_client():
    if bigquery_client is None:
        bigquery_client = bigquery.Client()
        print("Creating bigquery client...")
    return bigquery_client 


def get_tokens_table_path():
    client = get_bigquery_client()
    return f"{client.project}.datawarehouse.tokens"

# TOKENS_TABLE_PATH = f"{bigquery_client.project}.datawarehouse.tokens"



