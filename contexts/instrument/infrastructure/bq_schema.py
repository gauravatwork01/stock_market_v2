from google.cloud import bigquery

SCHEMA = [
    bigquery.SchemaField("instr_token", "INTEGER"),
    bigquery.SchemaField("symbol", "STRING"),
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("exchange", "STRING"),
    bigquery.SchemaField("created_at", "DATETIME"),
    bigquery.SchemaField("updated_at", "DATETIME"),
]

TABLE_SCHEMA = {
    "table_name" : "instrument",
    "fields" : [
        {"name": "instr_token", "type": "INTEGER"},
        {"name": "symbol", "type": "STRING"},
        {"name": "name", "type": "STRING"},
        {"name": "exchange", "type": "STRING"},
        {"name": "created_at", "type": "DATETIME"},
        {"name": "updated_at", "type": "DATETIME"}
    ]
}
