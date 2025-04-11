import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_bbc_news():
    """A simple function to scrape BBC News homepage."""
    print("Step 1: Connecting to BBC News website...")
    
    # Step 1: Make a request to BBC News
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    
    print("Step 2: Reading the webpage content...")
    # Step 2: Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("Step 3: Finding news articles...")
    # Step 3: Find all news articles
    articles = []
    for article in soup.find_all('div', class_='gs-c-promo'):
        title = article.find('h3')
        if title:
            articles.append({
                'title': title.text.strip(),
                'link': article.find('a')['href'] if article.find('a') else None,
                'collected_at': datetime.now().isoformat()
            })
    
    print(f"Step 4: Found {len(articles)} articles!")
    
    # Step 5: Save to a file (instead of cloud storage for now)
    print("Step 5: Saving to a file...")
    with open('bbc_news.json', 'w') as f:
        json.dump(articles, f, indent=2)
    
    print("Done! Check bbc_news.json for the results!")

if __name__ == "__main__":
    scrape_bbc_news() 