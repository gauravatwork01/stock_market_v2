


from google.cloud import bigquery

print("Creating bigquery client...")

bigquery = bigquery
bigquery_client = bigquery.Client()

TABLE_PATH = f"{bigquery_client.project_id}.datawarehouse.{{}}"

TOKENS_TABLE_PATH = f"{bigquery_client.project_id}.datawarehouse.tokens"



