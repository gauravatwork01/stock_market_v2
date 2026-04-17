


from google.cloud import bigquery

print("Creating bigquery client...")

bigquery = bigquery
bigquery_client = bigquery.Client()

TOKENS_TABLE_PATH = f"{bigquery_client.project}.datawarehouse.tokens"



