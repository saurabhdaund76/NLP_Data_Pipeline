import asyncio
import yaml
from src.collectors.web.news_scraper import NewsScraper
from src.storage.gcs.gcs_storage import GCSStorage

async def main():
    # Step 1: Load configuration
    with open('config/news_scraper_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Step 2: Initialize scraper for BBC News
    bbc_config = config['bbc_news']
    async with NewsScraper(bbc_config) as scraper:
        # Step 3: Collect data
        print("Scraping BBC News...")
        data = await scraper.collect()
        
        # Step 4: Validate data
        if await scraper.validate(data):
            print("Data validation successful!")
            
            # Step 5: Initialize storage
            storage_config = config['storage']['gcs']
            storage = GCSStorage(storage_config)
            
            # Step 6: Store data
            print("Storing data in Google Cloud Storage...")
            success = await storage.store(data['data'], data['metadata'])
            
            if success:
                print("Data stored successfully!")
                print(f"Storage location: {data['metadata'].get('storage_location')}")
            else:
                print("Failed to store data")
        else:
            print("Data validation failed!")

if __name__ == "__main__":
    asyncio.run(main()) 