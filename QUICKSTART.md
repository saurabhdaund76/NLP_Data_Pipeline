# Quick Start Guide

This guide will help you get started with the NLP Data Collection Pipeline in 15 minutes.

## 1. Prerequisites Installation (5 minutes)

### Install Python
- Download Python 3.8+ from [python.org](https://python.org)
- Verify installation:
  ```bash
  python --version
  ```

### Install Git
- Download Git from [git-scm.com](https://git-scm.com)
- Verify installation:
  ```bash
  git --version
  ```

## 2. Google Cloud Setup (5 minutes)

### Quick Setup Steps
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Start Free"
3. Get $300 free credits
4. Create project "nlp-data-pipeline"
5. Enable Cloud Storage API
6. Create service account and download key

### One-Click Setup
```bash
# After downloading service account key
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
```

## 3. Project Setup (5 minutes)

### Clone and Setup
```bash
# Clone repository
git clone <repository-url>
cd nlp-data-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configure
Create `.env` file:
```env
GOOGLE_APPLICATION_CREDENTIALS="./service-account-key.json"
GCP_PROJECT_ID="your-project-id"
GCP_BUCKET_NAME="nlp-data-pipeline-bucket"
NEWS_API_KEY="your-newsapi-key"
```

## 4. Test Setup

Run the test script:
```bash
python nlp_data_pipeline/examples/test_setup.py
```

## 5. First Data Collection

### Collect News Data
```python
from src.collectors.web.news_scraper import NewsScraper
from src.storage.gcs_storage import GCSStorage

# Initialize
scraper = NewsScraper(config)
storage = GCSStorage(config)

# Collect and store
data = scraper.scrape_article("https://www.bbc.com/news/example")
storage.store_data(data, "bbc_news")
```

## Next Steps
1. Check the main README.md for detailed documentation
2. Explore example scripts in `examples/` directory
3. Add more data sources
4. Customize configuration

## Common Issues

### Authentication Error
```bash
# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
```

### Storage Error
- Verify bucket name in `.env`
- Check permissions in Google Cloud Console

### API Rate Limit
- Check News API dashboard for usage
- Wait for quota reset

## Getting Help
- Check logs in `logs/pipeline.log`
- Review documentation
- Open an issue on GitHub 