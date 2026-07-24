from google.cloud import bigquery

HIST_SCHEMA = [
    bigquery.SchemaField("instr_token", "INTEGER"),
    bigquery.SchemaField("symbol", "STRING"),
    bigquery.SchemaField("interval", "STRING"),
    bigquery.SchemaField("open", "FLOAT"),
    bigquery.SchemaField("high", "FLOAT"),
    bigquery.SchemaField("low", "FLOAT"),
    bigquery.SchemaField("close", "FLOAT"),
    bigquery.SchemaField("datetime", "DATETIME"),
    bigquery.SchemaField("date", "DATE"),
]



