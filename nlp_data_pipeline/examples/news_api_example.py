import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime

def get_news():
    """A simple function to get news using NewsAPI."""
    print("Step 1: Loading API key from .env file...")
    
    # Step 1: Load environment variables
    load_dotenv()
    api_key = os.getenv('NEWS_API_KEY')
    
    print("Step 2: Making request to NewsAPI...")
    # Step 2: Make request to NewsAPI
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'us',
        'apiKey': api_key
    }
    
    response = requests.get(url, params=params)
    
    print("Step 3: Processing the response...")
    # Step 3: Process the response
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        
        # Format the articles
        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                'title': article.get('title'),
                'description': article.get('description'),
                'url': article.get('url'),
                'published_at': article.get('publishedAt'),
                'collected_at': datetime.now().isoformat()
            })
        
        print(f"Step 4: Found {len(formatted_articles)} articles!")
        
        # Step 5: Save to a file
        print("Step 5: Saving to a file...")
        with open('news_api_results.json', 'w') as f:
            json.dump(formatted_articles, f, indent=2)
        
        print("Done! Check news_api_results.json for the results!")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    get_news() 