"""
Base collector module that defines the interface for all data collectors.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime

class BaseCollector(ABC):
    """
    Abstract base class for all data collectors.
    
    This class defines the interface that all collector implementations must follow.
    It provides basic functionality for data collection, validation, and preprocessing.
    
    Attributes:
        name (str): Name of the collector
        config (Dict): Configuration parameters
        last_collection_time (datetime): Timestamp of last data collection
    """
    
    def __init__(self, name: str, config: Optional[Dict] = None):
        """
        Initialize the collector.
        
        Args:
            name: Unique name for the collector
            config: Configuration dictionary for the collector
        """
        self.name = name
        self.config = config or {}
        self.last_collection_time = None
        
    @abstractmethod
    def collect_data(self, *args, **kwargs) -> List[Dict]:
        """
        Collect data from the source.
        
        This method must be implemented by all collector classes.
        
        Returns:
            List of dictionaries containing collected data
        
        Raises:
            NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError("Collector must implement collect_data method")
    
    def validate_data(self, data: List[Dict]) -> bool:
        """
        Validate collected data.
        
        Args:
            data: List of dictionaries to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        if not isinstance(data, list):
            return False
        
        if not all(isinstance(item, dict) for item in data):
            return False
            
        return True
    
    def preprocess(self, data: List[Dict]) -> List[Dict]:
        """
        Preprocess collected data before storage.
        
        Args:
            data: Raw data to preprocess
            
        Returns:
            Preprocessed data
        """
        processed = []
        for item in data:
            # Add metadata
            item['collector_name'] = self.name
            item['collection_time'] = datetime.now().isoformat()
            
            # Remove None values
            processed_item = {
                k: v for k, v in item.items() 
                if v is not None
            }
            processed.append(processed_item)
            
        return processed
    
    def collect_and_process(self, *args, **kwargs) -> List[Dict]:
        """
        Collect, validate, and preprocess data.
        
        This is a convenience method that combines collection, validation,
        and preprocessing in one step.
        
        Returns:
            Processed data ready for storage
            
        Raises:
            ValueError: If collected data is invalid
        """
        # Collect raw data
        raw_data = self.collect_data(*args, **kwargs)
        
        # Validate
        if not self.validate_data(raw_data):
            raise ValueError(f"Invalid data collected by {self.name}")
        
        # Preprocess
        processed_data = self.preprocess(raw_data)
        
        # Update last collection time
        self.last_collection_time = datetime.now()
        
        return processed_data
    
    def get_collection_status(self) -> Dict:
        """
        Get status information about the collector.
        
        Returns:
            Dictionary containing collector status
        """
        return {
            'name': self.name,
            'last_collection_time': self.last_collection_time,
            'config': self.config
        }
    
    def __repr__(self) -> str:
        """String representation of the collector."""
        return f"{self.__class__.__name__}(name='{self.name}')" 