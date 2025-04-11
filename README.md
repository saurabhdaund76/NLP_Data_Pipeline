# NLP Data Collection Pipeline

A comprehensive data collection pipeline for gathering and storing data from multiple sources in Google Cloud Storage.

## Features
- Multi-source data collection (News API, Web Scraping, PDFs)
- Google Cloud Storage integration
- Error handling and logging
- Scalable architecture
- Easy configuration

## Quick Start
```bash
# Clone the repository
git clone https://github.com/your-username/nlp-data-pipeline.git
cd nlp-data-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp .env.example .env
# Edit .env with your credentials
```

## Documentation
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Hands-on Guide](docs/HANDS_ON_GUIDE.md)

## Prerequisites
- Python 3.8+
- Google Cloud account
- News API account
- Git

## Project Structure
```
nlp_data_pipeline/
├── src/               # Main code
├── config/            # Configuration files
├── examples/          # Example scripts
└── logs/             # Log files
```

## Configuration
1. Set up Google Cloud credentials
2. Configure News API key
3. Update storage settings

## Usage Examples
```python
# Collect news data
from src.collectors.web.news_scraper import NewsScraper
scraper = NewsScraper(config)
data = scraper.scrape_article(url)

# Store in Google Cloud
from src.storage.gcs_storage import GCSStorage
storage = GCSStorage(config)
storage.store_data(data, "news")
```

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License
MIT License - See [LICENSE](LICENSE) file

## Contact
- Create an issue for bug reports or feature requests
- Submit PRs for any improvements 