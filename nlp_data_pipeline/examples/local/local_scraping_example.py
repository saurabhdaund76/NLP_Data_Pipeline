"""
Example demonstrating web scraping with local storage.
"""

import os
from typing import Dict, List
from ...src.collectors.web.news_scraper import NewsScraper
from ...src.storage.local.local_storage import LocalStorage
from ...src.collectors.api.news_api_collector import NewsAPICollector

def scrape_and_store_locally():
    """Example function to demonstrate scraping and local storage."""
    
    # Initialize local storage
    storage = LocalStorage(base_path="data/news_articles")
    
    # Initialize scrapers
    news_scraper = NewsScraper()
    news_api = NewsAPICollector(api_key="YOUR_API_KEY")  # Replace with your API key
    
    # Scrape news from websites
    scraped_articles = news_scraper.collect_data([
        "https://example-news-site.com/technology",
        "https://another-news-site.com/ai"
    ])
    
    # Get news from API
    api_articles = news_api.collect_data(
        keywords=["artificial intelligence", "machine learning"],
        from_date="2024-01-01",
        to_date="2024-12-31"
    )
    
    # Save scraped articles as JSON
    scraped_path = storage.save_json(
        data=scraped_articles,
        prefix="web_scraped_news",
        directory="raw"
    )
    print(f"Saved scraped articles to: {scraped_path}")
    
    # Save API articles as CSV
    api_path = storage.save_csv(
        data=api_articles,
        prefix="api_news",
        directory="raw"
    )
    print(f"Saved API articles to: {api_path}")
    
    # Process and combine data
    all_articles = process_articles(scraped_articles + api_articles)
    
    # Save processed data
    processed_path = storage.save_json(
        data=all_articles,
        prefix="processed_news",
        directory="processed"
    )
    print(f"Saved processed articles to: {processed_path}")
    
    # Save metadata
    metadata = create_metadata(scraped_articles, api_articles)
    metadata_path = storage.save_json(
        data=metadata,
        prefix="news_metadata",
        directory="metadata"
    )
    print(f"Saved metadata to: {metadata_path}")

def process_articles(articles: List[Dict]) -> List[Dict]:
    """
    Process articles by cleaning and standardizing data.
    
    Args:
        articles: List of article dictionaries
        
    Returns:
        Processed articles
    """
    processed = []
    for article in articles:
        processed_article = {
            "title": clean_text(article.get("title", "")),
            "content": clean_text(article.get("content", "")),
            "date": standardize_date(article.get("date", "")),
            "source": article.get("source", "unknown"),
            "url": article.get("url", ""),
            "keywords": extract_keywords(article.get("content", ""))
        }
        processed.append(processed_article)
    return processed

def create_metadata(scraped: List[Dict], api: List[Dict]) -> Dict:
    """
    Create metadata about the collected articles.
    
    Args:
        scraped: Scraped articles
        api: API articles
        
    Returns:
        Metadata dictionary
    """
    return {
        "total_articles": len(scraped) + len(api),
        "scraped_count": len(scraped),
        "api_count": len(api),
        "sources": list(set(
            [article.get("source", "unknown") for article in scraped + api]
        )),
        "date_range": {
            "earliest": min([article.get("date", "9999") for article in scraped + api]),
            "latest": max([article.get("date", "0000") for article in scraped + api])
        }
    }

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Add your text cleaning logic here
    return text.strip()

def standardize_date(date_str: str) -> str:
    """Standardize date format."""
    # Add your date standardization logic here
    return date_str

def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text."""
    # Add your keyword extraction logic here
    return []

if __name__ == "__main__":
    scrape_and_store_locally() 