import logging
from src.collectors.web.news_scraper import NewsScraper

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    # Configuration for BBC News
    config = {
        'base_url': 'https://www.bbc.com/news',
        'selectors': {
            'title': 'h1.story-body__h1',
            'content': 'div.story-body__inner p',
            'date': 'div.date',
            'author': 'span.byline__name'
        }
    }
    
    # Initialize the scraper
    scraper = NewsScraper(config)
    
    # Example article URL
    article_url = 'https://www.bbc.com/news/technology-12345678'
    
    # Scrape the article
    print("Scraping article...")
    article_data = scraper.scrape_article(article_url)
    
    if article_data:
        print("\nScraped Data:")
        print(f"Title: {article_data['title']}")
        print(f"Author: {article_data['author']}")
        print(f"Date: {article_data['date']}")
        print(f"URL: {article_data['url']}")
        
        # Save to file
        filename = 'scraped_article.json'
        if scraper.save_to_file(article_data, filename):
            print(f"\nData saved to {filename}")
        else:
            print("\nFailed to save data")
    else:
        print("Failed to scrape article")

if __name__ == "__main__":
    main() 