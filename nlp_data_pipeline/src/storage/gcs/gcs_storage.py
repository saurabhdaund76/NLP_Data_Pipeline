import json
from typing import Any, Dict, Optional
from datetime import datetime
from google.cloud import storage
from ...storage.base import BaseStorage

class GCSStorage(BaseStorage):
    """Google Cloud Storage implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.bucket_name = config.get('bucket_name')
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)

    def _generate_blob_name(self, metadata: Dict[str, Any]) -> str:
        """Generate a unique blob name based on metadata."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        source = metadata.get('source', 'unknown')
        return f"{source}/{timestamp}.json"

    async def store(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> bool:
        """Store data in Google Cloud Storage."""
        try:
            blob_name = self._generate_blob_name(metadata)
            blob = self.bucket.blob(blob_name)
            
            # Combine data and metadata
            storage_data = {
                'data': data,
                'metadata': {
                    **metadata,
                    'stored_at': datetime.now().isoformat(),
                    'storage_location': f"gs://{self.bucket_name}/{blob_name}"
                }
            }
            
            # Upload as JSON
            blob.upload_from_string(
                json.dumps(storage_data),
                content_type='application/json'
            )
            
            self.update_stats(successful=True)
            return True
            
        except Exception as e:
            self.update_stats(successful=False)
            return False

    async def retrieve(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Retrieve data from Google Cloud Storage."""
        try:
            blob = self.bucket.blob(identifier)
            if not blob.exists():
                return None
                
            content = blob.download_as_string()
            return json.loads(content)
            
        except Exception:
            return None 