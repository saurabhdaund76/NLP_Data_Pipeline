from typing import Any, Dict, Optional
from datetime import datetime
import aiohttp
from ..base import BaseCollector

class NewsAPICollector(BaseCollector):
    """Collector for NewsAPI.
    
    This collector demonstrates how to:
    1. Connect to a REST API
    2. Handle API authentication
    3. Process paginated responses
    4. Handle rate limiting
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.base_url = "https://newsapi.org/v2"
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {
            'X-Api-Key': self.api_key,
            'User-Agent': 'NLP-Data-Pipeline/1.0'
        }

    async def __aenter__(self):
        """Initialize the HTTP session when entering the context."""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up the HTTP session when exiting the context."""
        if self.session:
            await self.session.close()

    async def _fetch_articles(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch articles from NewsAPI.
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            
        Returns:
            Dictionary containing articles and metadata
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:
                    # Rate limit exceeded
                    return {'status': 'error', 'message': 'Rate limit exceeded'}
                else:
                    return {'status': 'error', 'message': f'HTTP {response.status}'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    async def collect(self) -> Dict[str, Any]:
        """Collect news articles from NewsAPI.
        
        Supports different endpoints:
        - top-headlines
        - everything
        - sources
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context manager.")

        try:
            # Get configuration
            endpoint = self.config.get('endpoint', 'top-headlines')
            params = self.config.get('params', {})
            
            # Fetch articles
            response = await self._fetch_articles(endpoint, params)
            
            if response.get('status') == 'ok':
                self.update_stats(successful=True)
                return {
                    'data': response.get('articles', []),
                    'metadata': {
                        'source': 'newsapi',
                        'endpoint': endpoint,
                        'collected_at': datetime.now().isoformat(),
                        'status': 'success',
                        'total_results': response.get('totalResults', 0),
                        'data_type': 'news_articles'
                    }
                }
            else:
                self.update_stats(successful=False)
                return {
                    'data': None,
                    'metadata': {
                        'source': 'newsapi',
                        'collected_at': datetime.now().isoformat(),
                        'status': 'error',
                        'error': response.get('message', 'Unknown error')
                    }
                }
                
        except Exception as e:
            self.update_stats(successful=False)
            return {
                'data': None,
                'metadata': {
                    'source': 'newsapi',
                    'collected_at': datetime.now().isoformat(),
                    'status': 'error',
                    'error': str(e)
                }
            }

    async def validate(self, data: Dict[str, Any]) -> bool:
        """Validate the collected data.
        
        Checks if articles are present and have required fields.
        """
        if not data or 'data' not in data:
            return False
            
        articles = data['data']
        if not isinstance(articles, list):
            return False
            
        required_fields = ['title', 'description', 'url']
        return all(
            all(field in article for field in required_fields)
            for article in articles
        ) 