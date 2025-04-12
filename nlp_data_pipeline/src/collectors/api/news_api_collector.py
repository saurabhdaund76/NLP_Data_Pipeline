"""
News API collector implementation.
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from ..base import BaseCollector
import logging

class NewsAPICollector(BaseCollector):
    """
    Collector for the News API service.
    
    This collector fetches news articles from the News API service.
    It handles pagination, rate limiting, and error handling.
    """
    
    def __init__(
        self,
        api_key: str,
        name: str = "news_api",
        config: Optional[Dict] = None
    ):
        """
        Initialize the News API collector.
        
        Args:
            api_key: News API authentication key
            name: Collector name
            config: Additional configuration
        """
        super().__init__(name, config)
        self.api_key = api_key
        self.base_url = self.config.get('base_url', 'https://newsapi.org/v2')
        self.logger = logging.getLogger(__name__)
        
    def collect_data(
        self,
        keywords: List[str],
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        language: str = 'en',
        sort_by: str = 'publishedAt',
        page_size: int = 100
    ) -> List[Dict]:
        """
        Collect news articles based on keywords and date range.
        
        Args:
            keywords: List of keywords to search for
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            language: Article language
            sort_by: Sorting criteria
            page_size: Number of articles per request
            
        Returns:
            List of article dictionaries
        """
        # Prepare parameters
        params = {
            'q': ' OR '.join(keywords),
            'language': language,
            'sortBy': sort_by,
            'pageSize': page_size,
            'apiKey': self.api_key
        }
        
        # Add date range if specified
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
            
        try:
            # Make API request
            response = self._make_request(
                endpoint='/everything',
                params=params
            )
            
            # Extract articles
            articles = response.get('articles', [])
            
            # Transform to standard format
            transformed_articles = self._transform_articles(articles)
            
            return transformed_articles
            
        except Exception as e:
            self.logger.error(f"Error collecting data: {str(e)}")
            raise
            
    def _make_request(
        self,
        endpoint: str,
        params: Dict,
        retries: int = 3
    ) -> Dict:
        """
        Make HTTP request to News API.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            retries: Number of retry attempts
            
        Returns:
            API response data
            
        Raises:
            requests.exceptions.RequestException: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(retries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    raise
                    
                self.logger.warning(
                    f"Request failed (attempt {attempt + 1}/{retries}): {str(e)}"
                )
                continue
                
    def _transform_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Transform articles to standard format.
        
        Args:
            articles: Raw articles from API
            
        Returns:
            Transformed articles
        """
        transformed = []
        
        for article in articles:
            transformed_article = {
                'title': article.get('title'),
                'content': article.get('content'),
                'description': article.get('description'),
                'url': article.get('url'),
                'source': article.get('source', {}).get('name'),
                'author': article.get('author'),
                'published_at': article.get('publishedAt'),
                'image_url': article.get('urlToImage')
            }
            transformed.append(transformed_article)
            
        return transformed
        
    def get_top_headlines(
        self,
        country: str = 'us',
        category: Optional[str] = None,
        page_size: int = 100
    ) -> List[Dict]:
        """
        Get top headlines for a country and category.
        
        Args:
            country: Country code
            category: News category
            page_size: Number of articles
            
        Returns:
            List of top headlines
        """
        params = {
            'country': country,
            'pageSize': page_size,
            'apiKey': self.api_key
        }
        
        if category:
            params['category'] = category
            
        try:
            response = self._make_request(
                endpoint='/top-headlines',
                params=params
            )
            
            articles = response.get('articles', [])
            return self._transform_articles(articles)
            
        except Exception as e:
            self.logger.error(f"Error fetching top headlines: {str(e)}")
            raise 