from typing import Any, Dict, Optional
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
from ..base import BaseCollector
import requests
import json
import logging

class NewsScraper(BaseCollector):
    """Collector for scraping news websites.
    
    This collector demonstrates how to:
    1. Connect to a website
    2. Parse HTML content
    3. Extract structured data
    4. Handle errors and retries
    5. Track scraping statistics
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get('base_url', '')
        self.selectors = config.get('selectors', {})  # CSS selectors for data extraction
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self):
        """Initialize the HTTP session when entering the context."""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up the HTTP session when exiting the context."""
        if self.session:
            await self.session.close()

    async def _fetch_page(self, url: str) -> Optional[str]:
        """Fetch the HTML content of a webpage.
        
        Args:
            url: The URL to fetch
            
        Returns:
            The HTML content as a string, or None if the fetch failed
        """
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                return None
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    async def _extract_data(self, html: str) -> Dict[str, Any]:
        """Extract structured data from HTML using BeautifulSoup.
        
        Args:
            html: The HTML content to parse
            
        Returns:
            A dictionary containing the extracted data
        """
        soup = BeautifulSoup(html, 'html.parser')
        extracted_data = {}
        
        # Extract article title
        if 'title' in self.selectors:
            title_elem = soup.select_one(self.selectors['title'])
            extracted_data['title'] = title_elem.text.strip() if title_elem else None
            
        # Extract article content
        if 'content' in self.selectors:
            content_elem = soup.select_one(self.selectors['content'])
            extracted_data['content'] = content_elem.text.strip() if content_elem else None
            
        # Extract publication date
        if 'date' in self.selectors:
            date_elem = soup.select_one(self.selectors['date'])
            extracted_data['date'] = date_elem.text.strip() if date_elem else None
            
        # Extract author
        if 'author' in self.selectors:
            author_elem = soup.select_one(self.selectors['author'])
            extracted_data['author'] = author_elem.text.strip() if author_elem else None
            
        return extracted_data

    async def collect(self) -> Dict[str, Any]:
        """Main collection method that orchestrates the scraping process.
        
        Steps:
        1. Fetch the webpage
        2. Parse the HTML
        3. Extract the data
        4. Package with metadata
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context manager.")

        try:
            # Step 1: Fetch the webpage
            html = await self._fetch_page(self.base_url)
            if not html:
                self.update_stats(successful=False)
                return {
                    'data': None,
                    'metadata': {
                        'source': self.base_url,
                        'collected_at': datetime.now().isoformat(),
                        'status': 'error',
                        'error': 'Failed to fetch webpage'
                    }
                }

            # Step 2 & 3: Parse and extract data
            extracted_data = await self._extract_data(html)
            
            # Step 4: Package with metadata
            self.update_stats(successful=True)
            return {
                'data': extracted_data,
                'metadata': {
                    'source': self.base_url,
                    'collected_at': datetime.now().isoformat(),
                    'status': 'success',
                    'data_type': 'news_article',
                    'extraction_method': 'web_scraping'
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
        """Validate the scraped data.
        
        Checks if essential fields are present and not empty.
        """
        if not data or 'data' not in data:
            return False
            
        extracted_data = data['data']
        required_fields = ['title', 'content']
        
        return all(
            field in extracted_data and 
            extracted_data[field] is not None and 
            extracted_data[field].strip() != ''
            for field in required_fields
        )

    def scrape_article(self, url):
        """Scrape a single article."""
        try:
            # Make the request
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data using selectors
            article_data = {
                'title': self._extract_text(soup, self.selectors.get('title')),
                'content': self._extract_text(soup, self.selectors.get('content')),
                'date': self._extract_text(soup, self.selectors.get('date')),
                'author': self._extract_text(soup, self.selectors.get('author')),
                'url': url,
                'collected_at': datetime.now().isoformat()
            }
            
            return article_data
            
        except Exception as e:
            self.logger.error(f"Error scraping article {url}: {str(e)}")
            return None
            
    def _extract_text(self, soup, selector):
        """Extract text using a CSS selector."""
        if not selector:
            return None
            
        element = soup.select_one(selector)
        return element.text.strip() if element else None
        
    def save_to_file(self, data, filename):
        """Save scraped data to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Error saving to file {filename}: {str(e)}")
            return False 