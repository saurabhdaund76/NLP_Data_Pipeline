from google.cloud import storage
import json
from datetime import datetime
import logging

class GCSStorage:
    """Google Cloud Storage handler for storing scraped data."""
    
    def __init__(self, config):
        self.config = config
        self.bucket_name = config.get('bucket_name')
        self.project_id = config.get('project_id')
        self.client = storage.Client(project=self.project_id)
        self.bucket = self.client.bucket(self.bucket_name)
        self.logger = logging.getLogger(__name__)
        
    def store_data(self, data, source_name):
        """Store data in GCS bucket."""
        try:
            # Create a unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{source_name}/{timestamp}.json"
            
            # Create blob and upload
            blob = self.bucket.blob(filename)
            blob.upload_from_string(
                json.dumps(data, indent=2, ensure_ascii=False),
                content_type='application/json'
            )
            
            self.logger.info(f"Data stored in GCS: gs://{self.bucket_name}/{filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing data in GCS: {str(e)}")
            return False
            
    def list_files(self, source_name=None):
        """List files in the bucket."""
        try:
            blobs = self.bucket.list_blobs(prefix=source_name)
            return [blob.name for blob in blobs]
        except Exception as e:
            self.logger.error(f"Error listing files: {str(e)}")
            return [] 