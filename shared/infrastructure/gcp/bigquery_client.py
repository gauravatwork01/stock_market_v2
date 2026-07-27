from typing import Any, Dict, List, Optional
from google.cloud import bigquery
from google.cloud.exceptions import NotFound, BadRequest
import logging
import copy
from utilities.utilities import log_time
import uuid
logger = logging.getLogger(__name__)



class BigQueryTableClient:

    def __init__(self, bq_client: bigquery.Client) -> None:
        self.client = bq_client


    def load_table_from_json(self, load_job_config, table_id, rows):
        
        load_job = self.client.load_table_from_json(
            rows,
            table_id,
            job_config=load_job_config,
        )
        load_job.result()


    def create_table_from_schema(
        self,
        table_id,
        schema,
        partition_field = None,
        clustering_fields = None,
    ):
        table = bigquery.Table(table_id, schema=schema)

        if partition_field:
            part_type = None 
            if partition_field == "datetime":
                part_type = bigquery.TimePartitioningType.DAY

            table.time_partitioning = bigquery.TimePartitioning(
                type_ = part_type,
                field = partition_field,
            )

        if clustering_fields:
            table.clustering_fields = clustering_fields

        return self.client.create_table(table)


    def table_exists(self, tbl_id:str):
        try:
            table = self.client.get_table(tbl_id)
            return table
        except NotFound:
            return False

    
    def delete_table(self,tbl_id):
        self.client.delete_table(tbl_id)
         


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


    def get_job_config_for_filling_table(self):
        job_config = bigquery.LoadJobConfig(
            write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE,
            create_disposition = bigquery.CreateDisposition.CREATE_NEVER, 
            ignore_unknown_values = True, 
        )
        return job_config

    def get_job_config_with_schema(self,schema):
        job_config = bigquery.LoadJobConfig(
            schema = schema,
            write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE,
            create_disposition = bigquery.CreateDisposition.CREATE_NEVER, 
            ignore_unknown_values = True, 
        )
        return job_config


class BigQueryConnection:

    def __init__(self,bq_client) -> None:
        self.client = bq_client
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

    
    def execute_query_as_arrow(self, query, query_params=None):
        query_res = self.bq_connection.execute_query(
            query = query,
            query_params = query_params
        )

        return query_res.to_arrow()

    @log_time 
    def load_existing_table_from_json(self, table_id,schema, rows:list[dict]):

        job_config = self.bq_config.get_job_config_with_schema(schema)
        insert_job = self.client.load_table_from_json(
            rows,
            table_id,
            job_config=job_config
        ) 
        res = insert_job.result()
        print("Rows inserted successfully.")


    def get_or_create_table(
        self, 
        table_id, 
        schema,
        partition_field = None,
        clustering_fields = None
    ):
        
        table = self.bq_table_client.table_exists(table_id)
        if table:
            self._ensure_schema_columns(table, schema)
        else:
            table = self.bq_table_client.create_table_from_schema(
                table_id, 
                schema,
                partition_field = partition_field,
                clustering_fields = clustering_fields
            )
        return table


    def upsert_data_using_merge(
        self, 
        table_dets, 
        merge_query: str ,
        rows: list[dict]
    ):
        main_tbl_name = table_dets["name"]
        table_schema = table_dets["bq_schema"]
        partition_field = table_dets["partition_field"]
        clustering_fields = table_dets["clustering_fields"]

        main_tbl_id = self.bq_connection.get_table_id(main_tbl_name)
        main_table = self.get_or_create_table(
            main_tbl_id, table_schema, partition_field, clustering_fields
        )

        staging_tbl_name = f"{main_tbl_name}_staging_{uuid.uuid4().hex}"
        staging_tbl_id = self.bq_connection.get_table_id(staging_tbl_name)
        staging_table = self.get_or_create_table(
            staging_tbl_id, table_schema
        )
        self.load_existing_table_from_json(staging_tbl_id,table_schema, rows)
        merge_query = merge_query.format(
            main_tbl_id = main_tbl_id, 
            staging_tbl_id = staging_tbl_id
        )
        self.client.query(merge_query).result()
        print("Rows upserted successfully.")

        self.bq_table_client.delete_table(staging_tbl_id)




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
