import yaml
import logging
from src.collectors.web.news_scraper import NewsScraper
from src.storage.gcs_storage import GCSStorage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load configuration
    with open('config/news_scraper_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize GCS storage
    gcs_config = config['storage']['gcs']
    storage = GCSStorage(gcs_config)
    
    # Initialize scraper for BBC News
    bbc_config = config['bbc_news']
    scraper = NewsScraper(bbc_config)
    
    # Example article URL
    article_url = 'https://www.bbc.com/news/technology-12345678'
    
    # Scrape the article
    logger.info("Scraping article...")
    article_data = scraper.scrape_article(article_url)
    
    if article_data:
        logger.info("Article scraped successfully!")
        
        # Store in GCS
        success = storage.store_data(
            article_data,
            gcs_config['folders']['bbc_news']
        )
        
        if success:
            logger.info("Data stored in GCS successfully!")
            
            # List files in the bucket
            files = storage.list_files(gcs_config['folders']['bbc_news'])
            logger.info(f"Files in bucket: {files}")
        else:
            logger.error("Failed to store data in GCS")
    else:
        logger.error("Failed to scrape article")

if __name__ == "__main__":
    main() 