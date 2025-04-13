# NLP Data Pipeline Implementation Guide

## Table of Contents
1. [Project Structure](#project-structure)
2. [Base Classes Implementation](#base-classes-implementation)
3. [Collectors Implementation](#collectors-implementation)
4. [Storage Implementation](#storage-implementation)
5. [Configuration Management](#configuration-management)
6. [Error Handling and Logging](#error-handling-and-logging)

## Project Structure

```
nlp_data_pipeline/
├── src/
│   ├── collectors/
│   │   ├── base.py
│   │   ├── api/
│   │   ├── web/
│   │   └── file/
│   ├── storage/
│   │   ├── base.py
│   │   ├── local/
│   │   └── gcs/
│   └── processing/
├── config/
├── examples/
└── tests/
```

## Base Classes Implementation

### BaseCollector
The foundation for all data collectors in the project.

```python
class BaseCollector(ABC):
    def __init__(self, name: str, config: Optional[Dict] = None):
        self.name = name
        self.config = config or {}
        self.last_collection_time = None
        self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    def collect_data(self) -> List[Dict]:
        """Must be implemented by child classes"""
        pass
    
    def validate_data(self, data: List[Dict]) -> bool:
        """Validates collected data"""
        if not isinstance(data, list):
            self.logger.error("Data must be a list")
            return False
        return True
    
    def preprocess(self, data: List[Dict]) -> List[Dict]:
        """Preprocesses data before storage"""
        processed = []
        for item in data:
            item['collector_name'] = self.name
            item['collection_time'] = datetime.now().isoformat()
            processed.append(item)
        return processed
```

### BaseStorage
The foundation for all storage implementations.

```python
class BaseStorage(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.storage_stats = {
            'total_stored': 0,
            'successful': 0,
            'failed': 0,
            'last_store': None
        }
        self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    async def store(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> bool:
        """Must be implemented by child classes"""
        pass
    
    def update_stats(self, successful: bool = True):
        """Updates storage statistics"""
        self.storage_stats['total_stored'] += 1
        if successful:
            self.storage_stats['successful'] += 1
        else:
            self.storage_stats['failed'] += 1
        self.storage_stats['last_store'] = datetime.now()
```

## Collectors Implementation

### NewsAPICollector
Example of an API-based collector.

```python
class NewsAPICollector(BaseCollector):
    def __init__(self, api_key: str, config: Optional[Dict] = None):
        super().__init__("news_api", config)
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
    
    async def collect_data(self) -> List[Dict]:
        """Collects news data from the API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/everything",
                    params={
                        'apiKey': self.api_key,
                        'q': self.config.get('query', ''),
                        'from': self.config.get('from_date'),
                        'to': self.config.get('to_date')
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('articles', [])
                    else:
                        self.logger.error(f"API request failed: {response.status}")
                        return []
        except Exception as e:
            self.logger.error(f"Error collecting news: {str(e)}")
            return []
```

### PDFCollector
Example of a file-based collector.

```python
class PDFCollector(BaseCollector):
    def __init__(self, config: Dict[str, Any]):
        super().__init__("pdf_collector", config)
        self.max_pages = config.get('max_pages', 100)
    
    async def collect_data(self) -> List[Dict]:
        """Collects and processes PDF data"""
        try:
            pdf_url = self.config.get('url')
            if not pdf_url:
                raise ValueError("PDF URL not provided")
            
            # Download PDF
            pdf_content = await self._download_pdf(pdf_url)
            if not pdf_content:
                return []
            
            # Extract text
            extracted_data = self._extract_text(pdf_content)
            return [extracted_data]
            
        except Exception as e:
            self.logger.error(f"Error processing PDF: {str(e)}")
            return []
```

## Storage Implementation

### LocalStorage
Implementation for local file system storage.

```python
class LocalStorage(BaseStorage):
    def __init__(self, base_path: str = "data"):
        super().__init__({"base_path": base_path})
        self.base_path = base_path
        self._create_directory_structure()
    
    def _create_directory_structure(self):
        """Creates necessary directories"""
        directories = [
            self.base_path,
            os.path.join(self.base_path, "raw"),
            os.path.join(self.base_path, "processed")
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    async def store(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> bool:
        """Stores data locally"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_{timestamp}.json"
            filepath = os.path.join(self.base_path, "raw", filename)
            
            with open(filepath, 'w') as f:
                json.dump({
                    'data': data,
                    'metadata': metadata
                }, f)
            
            self.update_stats(successful=True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing data: {str(e)}")
            self.update_stats(successful=False)
            return False
```

### GCSStorage
Implementation for Google Cloud Storage.

```python
class GCSStorage(BaseStorage):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.bucket_name = config.get('bucket_name')
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)
    
    async def store(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> bool:
        """Stores data in Google Cloud Storage"""
        try:
            blob_name = self._generate_blob_name(metadata)
            blob = self.bucket.blob(blob_name)
            
            storage_data = {
                'data': data,
                'metadata': {
                    **metadata,
                    'stored_at': datetime.now().isoformat()
                }
            }
            
            blob.upload_from_string(
                json.dumps(storage_data),
                content_type='application/json'
            )
            
            self.update_stats(successful=True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing in GCS: {str(e)}")
            self.update_stats(successful=False)
            return False
```

## Configuration Management

### YAML Configuration
Example configuration file structure.

```yaml
# config/data_collectors_config.yaml
collectors:
  news_api:
    api_key: "your-api-key"
    endpoints:
      top_headlines:
        country: "us"
        category: "technology"
  web_scraping:
    bbc_news:
      base_url: "https://www.bbc.com/news"
      selectors:
        article: ".gs-c-promo"
        title: ".gs-c-promo-heading"
  pdf_collection:
    government_reports:
      url: "https://example.com/report.pdf"
      max_pages: 50

storage:
  gcs:
    bucket_name: "your-bucket-name"
    project_id: "your-project-id"
```

### Environment Variables
Using .env file for sensitive data.

```env
# .env
NEWS_API_KEY=your-api-key
GCS_BUCKET_NAME=your-bucket-name
GCS_PROJECT_ID=your-project-id
```

## Error Handling and Logging

### Custom Exceptions
Project-specific exceptions.

```python
class DataCollectionError(Exception):
    def __init__(self, message: str, source: str):
        self.message = message
        self.source = source
        super().__init__(f"{message} (Source: {source})")

class StorageError(Exception):
    def __init__(self, message: str, storage_type: str):
        self.message = message
        self.storage_type = storage_type
        super().__init__(f"{message} (Storage: {storage_type})")
```

### Logging Configuration
Setting up logging for the project.

```python
# src/utils/logging.py
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/pipeline.log'),
            logging.StreamHandler()
        ]
    )
```

## Best Practices

1. **Error Handling**
   - Always use try-except blocks
   - Log errors with context
   - Use custom exceptions
   - Implement retry mechanisms

2. **Logging**
   - Use appropriate log levels
   - Include context in log messages
   - Log to both file and console
   - Use structured logging

3. **Configuration**
   - Use YAML for complex config
   - Use .env for sensitive data
   - Validate configuration
   - Provide default values

4. **Code Organization**
   - Follow single responsibility principle
   - Use type hints
   - Document public interfaces
   - Write unit tests

## Next Steps

1. **Implementation**
   - Add more collectors
   - Implement additional storage options
   - Add data processing pipelines
   - Create monitoring tools

2. **Testing**
   - Write unit tests
   - Add integration tests
   - Implement CI/CD
   - Add performance tests

3. **Documentation**
   - Add API documentation
   - Create user guides
   - Document deployment process
   - Add troubleshooting guides 