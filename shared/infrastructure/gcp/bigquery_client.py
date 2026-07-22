from typing import Any, Dict, List, Optional
from google.cloud import bigquery
from google.cloud.exceptions import NotFound, BadRequest
import logging
import copy
import uuid
logger = logging.getLogger(__name__)


SCHEMA = {
    "composite_columns" : ["instr_token", "interval", "date_time"],
    "columns" : {
        "instr_token" : "INTEGER",
        "symbol" : "STRING",
        "name" : "STRING",
        "exchange" : "STRING",
        "created_at" : "DATETIME",
        "updated_at" : "DATETIME"
    },
    ""
}

def construct_merge_query_using_schema(schema, main_tbl, staging_tbl):
    comp_cols = schema["composite_columns"]
    joins_on_str = " AND ".join(f'M.{c} = S.{c}' for c in comp_cols)
    
    all_create_cols = list(schema["columns"].keys())
    create_cols_str = ",".join(all_create_cols)
    create_vals_str = ",".join(f"S.{col_name}" for col_name in all_create_cols)
     
    all_update_cols = copy.deepcopy(all_create_cols)
    all_update_cols.remove("created_at")
    update_str = ",".join(f"{col_name} = S.{col_name}" for col_name in all_update_cols)

    
    merge_query = f"""
        MERGE `{main_tbl}` M
        USING `{staging_tbl}` S
        ON {joins_on_str}
        WHEN MATCHED THEN UPDATE SET
            {update_str}
        WHEN NOT MATCHED THEN INSERT
            ({create_cols_str})
            VALUES
            ({create_vals_str})
    """
    return merge_query



class Schema:

    def __init__(self,schema) -> None:
        self.schema = schema 

    
    def parse_bq_schema(self):
        SCHEMA = []
        for col_name, data_type in self.schema["columns"].items():
            schema_field = bigquery.SchemaField(col_name, data_type)
            SCHEMA.append(schema_field)



class BigQueryTableClient:

    def __init__(self, bq_client: bigquery.Client) -> None:
        self.client = bq_client


    def create_new_table_from_json(self, load_job_config, table_id, rows):
        
        load_job = self.client.load_table_from_json(
            rows,
            table_id,
            job_config=load_job_config,
        )
        load_job.result()


    def create_table_from_schema(self,table_id, schema):
        table = bigquery.Table(table_id, schema=schema)
        self.client.create_table(table)


    def table_exists(self, tbl_id:str):
        try:
            table = self.client.get_table(tbl_id)
            return table
        except NotFound:
            return False


class BigQuerySchemaTranslator:
    """Translates your internal schema dict format into bigquery.SchemaField objects."""

    def __init__(self, schema_dict: dict):
        self.schema_dict = schema_dict

    def to_bq_schema(self) -> list[bigquery.SchemaField]:
        return [
            bigquery.SchemaField(col_name, data_type)
            for col_name, data_type in self.schema_dict["columns"].items()
        ]

    @property
    def composite_columns(self) -> list[str]:
        return self.schema_dict["composite_columns"]

    @property
    def column_names(self) -> list[str]:
        return list(self.schema_dict["columns"].keys())



class BigQueryConfig:

    def get_job_config_using_params(self, query_parameters):
        job_config = bigquery.QueryJobConfig(
            query_parameters = query_parameters
        )
        return job_config


    def get_job_config_using_schema(self, schema):
        job_config = bigquery.LoadJobConfig(
            schema = schema,
            # write_disposition = bigquery.WriteDisposition.WRITE_APPEND,
            write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE,
            create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED,  # default
        )
        return job_config


class BigQueryConnection:

    def __init__(self) -> None:
        # self.client = bigquery.Client()
        self.bq_config = BigQueryConfig()

    @property
    def project(self) -> str:
        return self.client.project 

    def _build_query_parameters(self, query_params):
        query_parameters = []

        for each_param in query_params:
            each_query_param = bigquery.ScalarQueryParameter(each_param[0], each_param[1], each_param[2])
            query_parameters.append(each_query_param)
        return query_parameters


    def _get_job_config(self, query_params):
        query_parameters = self._build_query_parameters(query_params)

        job_config = self.bq_config.get_job_config_using_params(query_parameters)
        return job_config

    def execute_query(self, query, query_params=None):
        if query_params is None:
            query_res = self.client.query(query).result()
        else:
            job_config = self._get_job_config(query_params)
            query_res = self.client.query(query, job_config=job_config).result()

        return query_res

    
    def get_table_id(self, table_name):
        dataset = "datawarehouse"
        tbl_id = f"{self.project}.{dataset}.{table_name}"
        return tbl_id




class BigQueryClient:
    """Wrapper for Google Cloud BigQuery operations."""

    def __init__(self):
        bq_client = bigquery.Client()
        self.bq_connection = BigQueryConnection(bq_client)
        self.bq_table_client = BigQueryTableClient(bq_client)
        self.bq_config = BigQueryConfig()


        self.client = bq_client

        self.bq_tbl_mgr = BigQueryTableClient(bq_client)


    @property
    def project(self) -> str:
        return self.bq_connection.project


    @property
    def project_id(self) -> str:
        return self.bq_connection.project


    def execute_query(self, query, query_params=None):
        query_res = self.bq_connection.execute_query(
            query = query,
            query_params = query_params
        )

        return query_res


    def insert_data_using_load_strategy(self, schema, rows:list[dict], table_name):

        job_config = self.bq_config.get_job_config_using_schema(schema)

        table_id = f"{self.project_id}.datawarehouse.{table_name}"
        insert_job = self.client.load_table_from_json(
            rows,
            table_id,
            job_config=job_config
        ) 
        res = insert_job.result()
        print("Rows inserted successfully.")


    def get_or_create_table(self, table_id, schema):
        table_exists = self.bq_table_client.table_exists(table_id)
        if table_exists is False:
            self.bq_table_client.create_table_from_schema(table_id, schema)
        pass 


    def upsert_data_using_merge(self, schema, rows: list[dict], table_name: str):
        
        main_table_id = self.bq_connection.get_table_id(
            table_name = table_name
        )
        main_table = self.bq_table_client.table_exists(main_table_id)
        if main_table is False:
            self.bq_table_client.create_table_from_schema(main_table_id, schema)


        staging_table_id = self.bq_connection.get_table_id(
            table_name = f"{table_name}_staging_{uuid.uuid4().hex}"
        )
        job_config = self.bq_config.get_job_config_using_schema(schema)
        self.bq_table_client.create_new_table_from_json(job_config, staging_table_id, rows)

        try:
            table = self.client.get_table(main_table_id)
            self._ensure_schema_columns(table, schema)
        except NotFound:
            pass 
            # table = bigquery.Table(main_table_id, schema=schema)
            # self.client.create_table(table)


        merge_query = construct_merge_query_using_schema(
            schema = schema,
            main_tbl = main_table_id,
            staging_tbl = staging_table
        )
        self.client.query(merge_query).result()
        print("Rows upserted successfully.")


    def _ensure_schema_columns(self, table: bigquery.Table, schema: list):
        """Add any columns present in schema but missing from the live BQ table."""
        existing = {field.name for field in table.schema}
        missing = [field for field in schema if field.name not in existing]
        if not missing:
            return

        table.schema = list(table.schema) + missing
        self.client.update_table(table, ["schema"])
        logger.info(
            "Added columns to %s.%s.%s: %s",
            table.project,
            table.dataset_id,
            table.table_id,
            [f.name for f in missing],
        )
