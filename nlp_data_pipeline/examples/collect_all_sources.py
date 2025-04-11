import asyncio
import yaml
from src.collectors.web.news_scraper import NewsScraper
from src.collectors.api.news_api_collector import NewsAPICollector
from src.collectors.file.pdf_collector import PDFCollector
from src.storage.gcs.gcs_storage import GCSStorage

async def collect_and_store(collector, storage, source_name):
    """Collect data from a source and store it."""
    print(f"\nCollecting data from {source_name}...")
    
    async with collector as collector_instance:
        # Collect data
        data = await collector_instance.collect()
        
        # Validate data
        if await collector_instance.validate(data):
            print(f"Data validation successful for {source_name}!")
            
            # Store data
            print(f"Storing {source_name} data...")
            success = await storage.store(data['data'], data['metadata'])
            
            if success:
                print(f"{source_name} data stored successfully!")
                print(f"Storage location: {data['metadata'].get('storage_location')}")
            else:
                print(f"Failed to store {source_name} data")
        else:
            print(f"Data validation failed for {source_name}!")

async def main():
    # Step 1: Load configuration
    with open('config/data_collectors_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Step 2: Initialize storage
    storage_config = config['storage']['gcs']
    storage = GCSStorage(storage_config)
    
    # Step 3: Collect from web scraping
    bbc_config = config['web_scraping']['bbc_news']
    await collect_and_store(NewsScraper(bbc_config), storage, "BBC News")
    
    # Step 4: Collect from NewsAPI
    news_api_config = {
        'api_key': config['news_api']['api_key'],
        **config['news_api']['endpoints']['top_headlines']
    }
    await collect_and_store(NewsAPICollector(news_api_config), storage, "NewsAPI")
    
    # Step 5: Collect PDFs
    pdf_config = config['pdf_collection']['government_reports']
    await collect_and_store(PDFCollector(pdf_config), storage, "Government Report PDF")

if __name__ == "__main__":
    asyncio.run(main()) 