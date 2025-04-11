import aiohttp
from typing import Any, Dict, Optional
from datetime import datetime
from ..base import BaseCollector

class RESTCollector(BaseCollector):
    """Collector for REST API endpoints."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.session: Optional[aiohttp.ClientSession] = None
        self.base_url = config.get('base_url', '')
        self.headers = config.get('headers', {})
        self.timeout = config.get('timeout', 30)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def collect(self) -> Dict[str, Any]:
        """Collect data from REST API endpoint."""
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context manager.")

        try:
            async with self.session.get(
                self.base_url,
                timeout=self.timeout
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.update_stats(successful=True)
                    return {
                        'data': data,
                        'metadata': {
                            'source': self.base_url,
                            'collected_at': datetime.now().isoformat(),
                            'status': 'success'
                        }
                    }
                else:
                    self.update_stats(successful=False)
                    return {
                        'data': None,
                        'metadata': {
                            'source': self.base_url,
                            'collected_at': datetime.now().isoformat(),
                            'status': 'error',
                            'error': f"HTTP {response.status}"
                        }
                    }
        except Exception as e:
            self.update_stats(successful=False)
            return {
                'data': None,
                'metadata': {
                    'source': self.base_url,
                    'collected_at': datetime.now().isoformat(),
                    'status': 'error',
                    'error': str(e)
                }
            }

    async def validate(self, data: Dict[str, Any]) -> bool:
        """Validate the collected data."""
        if not data or 'data' not in data:
            return False
        
        # Add specific validation logic based on your API response structure
        return True 