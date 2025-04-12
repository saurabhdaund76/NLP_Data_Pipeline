"""
Local storage implementation for storing scraped data in the local filesystem.
"""

import os
import json
import csv
import pickle
from datetime import datetime
from typing import Any, Dict, List, Union
from ..base import BaseStorage

class LocalStorage(BaseStorage):
    """
    Storage implementation for saving data to local filesystem.
    Supports multiple formats: JSON, CSV, Pickle, Text
    """

    def __init__(self, base_path: str = "data"):
        """
        Initialize local storage with base path.
        
        Args:
            base_path (str): Base directory for storing data
        """
        self.base_path = base_path
        self._create_directory_structure()

    def _create_directory_structure(self):
        """Create the necessary directory structure for data storage."""
        directories = [
            self.base_path,
            os.path.join(self.base_path, "raw"),
            os.path.join(self.base_path, "processed"),
            os.path.join(self.base_path, "metadata")
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def _get_timestamp_path(self, directory: str, prefix: str, extension: str) -> str:
        """Generate a timestamped filepath."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.{extension}"
        return os.path.join(directory, filename)

    def save_json(self, data: Union[Dict, List], prefix: str = "data", directory: str = "raw") -> str:
        """
        Save data as JSON file.
        
        Args:
            data: Data to save
            prefix: Prefix for the filename
            directory: Subdirectory under base_path
            
        Returns:
            str: Path to saved file
        """
        full_dir = os.path.join(self.base_path, directory)
        filepath = self._get_timestamp_path(full_dir, prefix, "json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath

    def save_csv(self, data: List[Dict], prefix: str = "data", directory: str = "raw") -> str:
        """
        Save data as CSV file.
        
        Args:
            data: List of dictionaries to save
            prefix: Prefix for the filename
            directory: Subdirectory under base_path
            
        Returns:
            str: Path to saved file
        """
        if not data:
            raise ValueError("No data to save")

        full_dir = os.path.join(self.base_path, directory)
        filepath = self._get_timestamp_path(full_dir, prefix, "csv")
        
        fieldnames = data[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        return filepath

    def save_pickle(self, data: Any, prefix: str = "data", directory: str = "raw") -> str:
        """
        Save data as pickle file.
        
        Args:
            data: Data to pickle
            prefix: Prefix for the filename
            directory: Subdirectory under base_path
            
        Returns:
            str: Path to saved file
        """
        full_dir = os.path.join(self.base_path, directory)
        filepath = self._get_timestamp_path(full_dir, prefix, "pkl")
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        
        return filepath

    def save_text(self, text: str, prefix: str = "data", directory: str = "raw") -> str:
        """
        Save text data to file.
        
        Args:
            text: Text to save
            prefix: Prefix for the filename
            directory: Subdirectory under base_path
            
        Returns:
            str: Path to saved file
        """
        full_dir = os.path.join(self.base_path, directory)
        filepath = self._get_timestamp_path(full_dir, prefix, "txt")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return filepath

    def load_json(self, filepath: str) -> Union[Dict, List]:
        """Load data from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_csv(self, filepath: str) -> List[Dict]:
        """Load data from CSV file."""
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def load_pickle(self, filepath: str) -> Any:
        """Load data from pickle file."""
        with open(filepath, 'rb') as f:
            return pickle.load(f)

    def load_text(self, filepath: str) -> str:
        """Load data from text file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def list_files(self, directory: str = "raw", extension: str = None) -> List[str]:
        """
        List all files in specified directory.
        
        Args:
            directory: Subdirectory under base_path
            extension: Filter by file extension
            
        Returns:
            List of file paths
        """
        full_dir = os.path.join(self.base_path, directory)
        files = os.listdir(full_dir)
        
        if extension:
            files = [f for f in files if f.endswith(f".{extension}")]
        
        return [os.path.join(full_dir, f) for f in files] 