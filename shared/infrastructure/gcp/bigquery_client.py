from typing import Any, Dict, List, Optional
from google.cloud import bigquery
from google.cloud.exceptions import NotFound, BadRequest
import logging

logger = logging.getLogger(__name__)


class BigQueryClient:
    """Wrapper for Google Cloud BigQuery operations."""

    def __init__(self):
        self.client = bigquery.Client()
        # self.project_id = self.client.project

    @property
    def project(self) -> str:
        return self.client.project 

    @property
    def project_id(self) -> str:
        return self.client.project 

    def build_query_parameters(self, query_params):
        query_parameters = []
        for each_param in query_params:
            each_query_param = bigquery.ScalarQueryParameter(each_param[0], each_param[1], each_param[2])
            query_parameters.append(each_query_param)
        
        return query_parameters


    def get_job_config(self, query_params):
        query_parameters = self.build_query_parameters(query_params)

        job_config = bigquery.QueryJobConfig(
            query_parameters = query_parameters
        )
        return job_config


    def execute_query(self, query, query_params=None):
        if query_params is None:
            query_res = self.client.query(query).result()
        else:
            job_config = self.get_job_config(query_params)
            query_res = self.client.query(query, job_config=job_config).result()

        return query_res


    def insert_data_using_load_strategy(self, schema, rows:list[dict], table_name):

        job_config = bigquery.LoadJobConfig(
            schema = schema,
            write_disposition = bigquery.WriteDisposition.WRITE_APPEND,
            create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED,  # default
        )

        table_id = f"{self.project_id}.datawarehouse.{table_name}"
        insert_job = self.client.load_table_from_json(
            rows,
            table_id,
            job_config=job_config
        ) 
        res = insert_job.result()
        print("Rows inserted successfully.")


    def upsert_data_using_merge(self, schema, rows: list[dict], table_name: str):
        dataset = "datawarehouse"
        target_table = f"{self.project_id}.{dataset}.{table_name}"
        staging_table = f"{self.project_id}.{dataset}.{table_name}_staging"

        load_job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
        )
        load_job = self.client.load_table_from_json(
            rows,
            staging_table,
            job_config=load_job_config,
        )
        load_job.result()

        try:
            table = self.client.get_table(target_table)
            self._ensure_schema_columns(table, schema)
        except NotFound:
            table = bigquery.Table(target_table, schema=schema)
            self.client.create_table(table)

        merge_query = f"""
            MERGE `{target_table}` T
            USING `{staging_table}` S
            ON T.instr_token = S.instr_token
            WHEN MATCHED THEN UPDATE SET
                symbol = S.symbol,
                name = S.name,
                exchange = S.exchange,
                updated_at = S.updated_at
            WHEN NOT MATCHED THEN INSERT
                (instr_token, symbol, name, exchange, created_at, updated_at)
                VALUES
                (S.instr_token, S.symbol, S.name, S.exchange, S.created_at, S.updated_at)
        """
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


"""
    def query_to_dataframe(self, sql: str) -> Any:
    
        try:
            query_job = self.query(sql)
            df = query_job.to_dataframe()
            logger.info(f"Query returned {len(df)} rows")
            return df
        except Exception as e:
            logger.error(f"Failed to convert query results to DataFrame: {e}")
            raise

    def insert_rows(self, table_id: str, rows: List[Dict[str, Any]]) -> List[Dict]:
        
        try:
            table = self.client.get_table(table_id)
            errors = self.client.insert_rows_json(table, rows)
            if errors:
                logger.error(f"Insert errors: {errors}")
            else:
                logger.info(f"Successfully inserted {len(rows)} rows into {table_id}")
            return errors
        except NotFound:
            logger.error(f"Table {table_id} not found")
            raise
        except Exception as e:
            logger.error(f"Failed to insert rows: {e}")
            raise

    def load_from_gcs(
        self,
        source_uri: str,
        table_id: str,
        job_config: Optional[bigquery.LoadJobConfig] = None,
    ) -> bigquery.LoadJob:
        
        try:
            if job_config is None:
                job_config = bigquery.LoadJobConfig()
            
            load_job = self.client.load_table_from_uri(source_uri, table_id, job_config=job_config)
            load_job.result()
            logger.info(f"Loaded {load_job.output_rows} rows from {source_uri} to {table_id}")
            return load_job
        except NotFound:
            logger.error(f"Table {table_id} not found")
            raise
        except Exception as e:
            logger.error(f"Failed to load data from GCS: {e}")
            raise

    def get_table(self, table_id: str) -> bigquery.Table:
       
        try:
            table = self.client.get_table(table_id)
            logger.info(f"Retrieved table {table_id}")
            return table
        except NotFound:
            logger.error(f"Table {table_id} not found")
            raise

    def list_tables(self, dataset_id: str) -> List[bigquery.TableListItem]:
       
        try:
            tables = self.client.list_tables(dataset_id)
            table_list = list(tables)
            logger.info(f"Found {len(table_list)} tables in {dataset_id}")
            return table_list
        except NotFound:
            logger.error(f"Dataset {dataset_id} not found")
            raise

    def create_table(self, table_id: str, schema: List[bigquery.SchemaField]) -> bigquery.Table:
     
        try:
            table = bigquery.Table(table_id, schema=schema)
            table = self.client.create_table(table)
            logger.info(f"Created table {table_id}")
            return table
        except Exception as e:
            logger.error(f"Failed to create table: {e}")
            raise

    def delete_table(self, table_id: str) -> None:
       
        try:
            self.client.delete_table(table_id)
            logger.info(f"Deleted table {table_id}")
        except NotFound:
            logger.error(f"Table {table_id} not found")
            raise

    def update_table(self, table: bigquery.Table) -> bigquery.Table:
      
        try:
            table = self.client.update_table(table, ["description", "labels"])
            logger.info(f"Updated table {table.project}.{table.dataset_id}.{table.table_id}")
            return table
        except Exception as e:
            logger.error(f"Failed to update table: {e}")
            raise

    def get_dataset(self, dataset_id: str) -> bigquery.Dataset:
       
        try:
            dataset = self.client.get_dataset(dataset_id)
            logger.info(f"Retrieved dataset {dataset_id}")
            return dataset
        except NotFound:
            logger.error(f"Dataset {dataset_id} not found")
            raise

    def list_datasets(self) -> List[bigquery.DatasetListItem]:
     
        try:
            datasets = self.client.list_datasets()
            dataset_list = list(datasets)
            logger.info(f"Found {len(dataset_list)} datasets in project {self.project_id}")
            return dataset_list
        except Exception as e:
            logger.error(f"Failed to list datasets: {e}")
            raise

    def create_dataset(self, dataset_id: str, location: str = "US") -> bigquery.Dataset:
    
        try:
            dataset = bigquery.Dataset(f"{self.project_id}.{dataset_id}")
            dataset.location = location
            dataset = self.client.create_dataset(dataset)
            logger.info(f"Created dataset {dataset_id}")
            return dataset
        except Exception as e:
            logger.error(f"Failed to create dataset: {e}")
            raise

    def delete_dataset(self, dataset_id: str, delete_contents: bool = False) -> None:
    
        try:
            self.client.delete_dataset(dataset_id, delete_contents=delete_contents)
            logger.info(f"Deleted dataset {dataset_id}")
        except NotFound:
            logger.error(f"Dataset {dataset_id} not found")
            raise

    def extract_to_gcs(
        self,
        table_id: str,
        destination_uri: str,
        job_config: Optional[bigquery.ExtractJobConfig] = None,
    ) -> bigquery.ExtractJob:
      
        try:
            if job_config is None:
                job_config = bigquery.ExtractJobConfig()
            
            extract_job = self.client.extract_table(table_id, destination_uri, job_config=job_config)
            extract_job.result()
            logger.info(f"Extracted {table_id} to {destination_uri}")
            return extract_job
        except NotFound:
            logger.error(f"Table {table_id} not found")
            raise
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            raise
"""