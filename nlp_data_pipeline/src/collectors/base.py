from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime

class BaseCollector(ABC):
    """Base class for all data collectors."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.last_run: Optional[datetime] = None
        self.collection_stats: Dict[str, Any] = {
            'total_items': 0,
            'successful': 0,
            'failed': 0,
            'last_run': None
        }

    @abstractmethod
    async def collect(self) -> Dict[str, Any]:
        """Collect data from the source.
        
        Returns:
            Dict containing the collected data and metadata
        """
        pass

    @abstractmethod
    async def validate(self, data: Dict[str, Any]) -> bool:
        """Validate the collected data.
        
        Args:
            data: The data to validate
            
        Returns:
            bool: True if data is valid, False otherwise
        """
        pass

    def update_stats(self, successful: bool = True):
        """Update collection statistics."""
        self.collection_stats['total_items'] += 1
        if successful:
            self.collection_stats['successful'] += 1
        else:
            self.collection_stats['failed'] += 1
        self.collection_stats['last_run'] = datetime.now()

    def get_stats(self) -> Dict[str, Any]:
        """Get current collection statistics."""
        return self.collection_stats 