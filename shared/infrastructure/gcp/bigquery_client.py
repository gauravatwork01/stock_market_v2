from typing import Any, Dict, List, Optional
from google.cloud import bigquery
from google.cloud.exceptions import NotFound, BadRequest
import logging

logger = logging.getLogger(__name__)


class BigQueryClient:
    """Wrapper for Google Cloud BigQuery operations."""

    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize BigQuery client.
        
        Args:
            project_id: GCP project ID. If None, uses default from credentials.
        """
        self.client = bigquery.Client(project=project_id)
        self.project_id = self.client.project

    def query(self, sql: str, job_config: Optional[bigquery.QueryJobConfig] = None) -> bigquery.QueryJob:
       
        try:
            job = self.client.query(sql, job_config=job_config)
            return job
        except BadRequest as e:
            logger.error(f"Bad query: {e}")
            raise
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def query_to_dataframe(self, sql: str) -> Any:
        """
        Execute query and return results as pandas DataFrame.
        
        Args:
            sql: SQL query string
            
        Returns:
            pandas DataFrame with query results
        """
        try:
            query_job = self.query(sql)
            df = query_job.to_dataframe()
            logger.info(f"Query returned {len(df)} rows")
            return df
        except Exception as e:
            logger.error(f"Failed to convert query results to DataFrame: {e}")
            raise

    def insert_rows(self, table_id: str, rows: List[Dict[str, Any]]) -> List[Dict]:
        """
        Insert rows into a BigQuery table.
        
        Args:
            table_id: Full table ID (project.dataset.table)
            rows: List of dictionaries representing rows to insert
            
        Returns:
            List of error dictionaries (empty if successful)
        """
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
        """
        Load data from Google Cloud Storage into BigQuery.
        
        Args:
            source_uri: GCS URI (gs://bucket/path/file)
            table_id: Full table ID (project.dataset.table)
            job_config: Optional LoadJobConfig for custom settings
            
        Returns:
            LoadJob object
        """
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
        """
        Get table metadata.
        
        Args:
            table_id: Full table ID (project.dataset.table)
            
        Returns:
            Table object with metadata
        """
        try:
            table = self.client.get_table(table_id)
            logger.info(f"Retrieved table {table_id}")
            return table
        except NotFound:
            logger.error(f"Table {table_id} not found")
            raise

    def list_tables(self, dataset_id: str) -> List[bigquery.TableListItem]:
        """
        List all tables in a dataset.
        
        Args:
            dataset_id: Dataset ID (project.dataset or just dataset)
            
        Returns:
            List of TableListItem objects
        """
        try:
            tables = self.client.list_tables(dataset_id)
            table_list = list(tables)
            logger.info(f"Found {len(table_list)} tables in {dataset_id}")
            return table_list
        except NotFound:
            logger.error(f"Dataset {dataset_id} not found")
            raise

    def create_table(self, table_id: str, schema: List[bigquery.SchemaField]) -> bigquery.Table:
        """
        Create a new table.
        
        Args:
            table_id: Full table ID (project.dataset.table)
            schema: List of SchemaField objects defining the table schema
            
        Returns:
            Created Table object
        """
        try:
            table = bigquery.Table(table_id, schema=schema)
            table = self.client.create_table(table)
            logger.info(f"Created table {table_id}")
            return table
        except Exception as e:
            logger.error(f"Failed to create table: {e}")
            raise

    def delete_table(self, table_id: str) -> None:
        """
        Delete a table.
        
        Args:
            table_id: Full table ID (project.dataset.table)
        """
        try:
            self.client.delete_table(table_id)
            logger.info(f"Deleted table {table_id}")
        except NotFound:
            logger.error(f"Table {table_id} not found")
            raise

    def update_table(self, table: bigquery.Table) -> bigquery.Table:
        """
        Update table properties.
        
        Args:
            table: Table object with updated properties
            
        Returns:
            Updated Table object
        """
        try:
            table = self.client.update_table(table, ["description", "labels"])
            logger.info(f"Updated table {table.project}.{table.dataset_id}.{table.table_id}")
            return table
        except Exception as e:
            logger.error(f"Failed to update table: {e}")
            raise

    def get_dataset(self, dataset_id: str) -> bigquery.Dataset:
        """
        Get dataset metadata.
        
        Args:
            dataset_id: Dataset ID (project.dataset or just dataset)
            
        Returns:
            Dataset object with metadata
        """
        try:
            dataset = self.client.get_dataset(dataset_id)
            logger.info(f"Retrieved dataset {dataset_id}")
            return dataset
        except NotFound:
            logger.error(f"Dataset {dataset_id} not found")
            raise

    def list_datasets(self) -> List[bigquery.DatasetListItem]:
        """
        List all datasets in the project.
        
        Returns:
            List of DatasetListItem objects
        """
        try:
            datasets = self.client.list_datasets()
            dataset_list = list(datasets)
            logger.info(f"Found {len(dataset_list)} datasets in project {self.project_id}")
            return dataset_list
        except Exception as e:
            logger.error(f"Failed to list datasets: {e}")
            raise

    def create_dataset(self, dataset_id: str, location: str = "US") -> bigquery.Dataset:
        """
        Create a new dataset.
        
        Args:
            dataset_id: Dataset ID
            location: Dataset location (default: US)
            
        Returns:
            Created Dataset object
        """
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
        """
        Delete a dataset.
        
        Args:
            dataset_id: Dataset ID
            delete_contents: If True, delete dataset even if it contains tables
        """
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
        """
        Extract table data to Google Cloud Storage.
        
        Args:
            table_id: Full table ID (project.dataset.table)
            destination_uri: GCS destination URI (gs://bucket/path/file)
            job_config: Optional ExtractJobConfig for custom settings
            
        Returns:
            ExtractJob object
        """
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
