import os
from google.cloud import bigquery
from google.cloud import storage
import logging
from datetime import datetime

class CloudDatabase:
    """Handler for cloud database operations."""
    
    def __init__(self, config):
        self.config = config
        self.project_id = config.get('project_id')
        self.dataset_id = config.get('dataset_id')
        self.bigquery_client = bigquery.Client(project=self.project_id)
        self.storage_client = storage.Client(project=self.project_id)
        self.logger = logging.getLogger(__name__)
        
    def create_table(self, table_name, schema):
        """Create a BigQuery table if it doesn't exist."""
        try:
            table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
            table = bigquery.Table(table_id, schema=schema)
            table = self.bigquery_client.create_table(table, exists_ok=True)
            self.logger.info(f"Table {table_id} created successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error creating table: {str(e)}")
            return False
            
    def insert_data(self, table_name, data):
        """Insert data into BigQuery table."""
        try:
            table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
            errors = self.bigquery_client.insert_rows_json(table_id, [data])
            if not errors:
                self.logger.info(f"Data inserted into {table_id} successfully")
                return True
            else:
                self.logger.error(f"Errors inserting data: {errors}")
                return False
        except Exception as e:
            self.logger.error(f"Error inserting data: {str(e)}")
            return False
            
    def query_data(self, query):
        """Execute a BigQuery query."""
        try:
            query_job = self.bigquery_client.query(query)
            results = query_job.result()
            return results
        except Exception as e:
            self.logger.error(f"Error executing query: {str(e)}")
            return None 