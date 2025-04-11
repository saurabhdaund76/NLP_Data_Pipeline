from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime

class BaseStorage(ABC):
    """Base class for all storage implementations."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.storage_stats: Dict[str, Any] = {
            'total_stored': 0,
            'successful': 0,
            'failed': 0,
            'last_store': None
        }

    @abstractmethod
    async def store(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> bool:
        """Store the collected data.
        
        Args:
            data: The data to store
            metadata: Additional metadata about the data
            
        Returns:
            bool: True if storage was successful, False otherwise
        """
        pass

    @abstractmethod
    async def retrieve(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored data.
        
        Args:
            identifier: Unique identifier for the data
            
        Returns:
            Optional[Dict]: The stored data if found, None otherwise
        """
        pass

    def update_stats(self, successful: bool = True):
        """Update storage statistics."""
        self.storage_stats['total_stored'] += 1
        if successful:
            self.storage_stats['successful'] += 1
        else:
            self.storage_stats['failed'] += 1
        self.storage_stats['last_store'] = datetime.now()

    def get_stats(self) -> Dict[str, Any]:
        """Get current storage statistics."""
        return self.storage_stats 