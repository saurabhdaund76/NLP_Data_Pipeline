# Understanding the Project Structure

This document explains each part of the NLP Data Collection Pipeline in detail, making it easy for newcomers to understand how everything works together.

## Table of Contents
1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Source Code (src/)](#source-code)
4. [Configuration (config/)](#configuration)
5. [Examples](#examples)
6. [Logging](#logging)
7. [How Everything Works Together](#how-everything-works-together)

## Overview

Think of this project as a data collection system with three main parts:
1. **Collectors** - Gather data from different sources
2. **Storage** - Save the data safely
3. **Configuration** - Control how everything works

## Directory Structure

Let's break down each folder and understand its purpose:

```
nlp_data_pipeline/
├── src/               # Main code (like the engine of a car)
├── config/            # Settings (like the control panel)
├── examples/          # Learning materials (like a user manual)
└── logs/             # Record keeping (like a black box)
```

## Source Code (src/)

### 1. Collectors (src/collectors/)
Think of collectors as workers, each specialized in getting data from different places:

```
collectors/
├── api/              # Gets data from web services
│   └── news_api_collector.py
├── web/              # Gets data from websites
│   └── news_scraper.py
└── file/             # Gets data from files
    └── pdf_collector.py
```

#### Example: News API Collector
```python
# src/collectors/api/news_api_collector.py
class NewsAPICollector:
    def collect_news(self):
        # Gets news articles from News API
        # Like asking a librarian for today's newspapers
```

### 2. Storage (src/storage/)
Think of storage as a filing system:

```
storage/
└── gcs_storage.py    # Stores data in Google Cloud
```

#### Example: Google Cloud Storage
```python
# src/storage/gcs_storage.py
class GCSStorage:
    def store_data(self, data):
        # Saves data to Google Cloud
        # Like filing documents in a cabinet
```

## Configuration (config/)

Think of configuration files as instruction manuals:

```yaml
# config/news_scraper_config.yaml
bbc_news:
  base_url: "https://www.bbc.com/news"  # Where to look
  selectors:
    title: "h1.story-body__h1"          # What to collect
```

### Why Configuration Files?
1. Easy to change settings without touching code
2. Keep sensitive information separate
3. Customize behavior for different situations

## Examples

Think of examples as cooking recipes - they show you how to use everything:

```
examples/
├── simple_example.py       # Basic recipe
├── news_api_example.py    # News API recipe
└── pdf_example.py         # PDF handling recipe
```

### Simple Example Explained
```python
# examples/simple_example.py

# 1. Get the tools ready
from src.collectors.web.news_scraper import NewsScraper
from src.storage.gcs_storage import GCSStorage

# 2. Set up the collector
scraper = NewsScraper(config)

# 3. Collect data
data = scraper.scrape_article(url)

# 4. Store the data
storage.store_data(data, "bbc_news")
```

## Logging

Think of logs as a diary that records everything that happens:

```
logs/
└── pipeline.log      # Records all activities
```

### Log Example
```
2024-01-20 10:30:15 INFO: Starting data collection
2024-01-20 10:30:16 INFO: Collected article: "Tech News Today"
2024-01-20 10:30:17 INFO: Stored article in Google Cloud
```

## How Everything Works Together

Let's follow a complete example:

1. **Start the Process**
   ```python
   # Load settings from config
   config = load_config('config/news_scraper_config.yaml')
   ```

2. **Collect Data**
   ```python
   # Use collector to get data
   collector = NewsCollector(config)
   data = collector.collect()
   ```

3. **Store Data**
   ```python
   # Save data to Google Cloud
   storage = GCSStorage(config)
   storage.store(data)
   ```

4. **Log Everything**
   ```python
   # Record what happened
   logger.info("Data collected and stored successfully")
   ```

### Visual Flow
```
Config File → Collector → Data → Storage → Google Cloud
     ↓           ↓         ↓        ↓
    Logs      Logs      Logs     Logs
```

## Common Use Cases

1. **Collecting News Articles**
   ```python
   # Example: Collect BBC News
   scraper = NewsScraper(config)
   articles = scraper.collect_news()
   storage.store(articles)
   ```

2. **Downloading PDFs**
   ```python
   # Example: Get government reports
   pdf_collector = PDFCollector(config)
   pdf_data = pdf_collector.download("report.pdf")
   storage.store(pdf_data)
   ```

## Best Practices

1. **Always Check Configuration**
   - Verify settings before running
   - Keep sensitive data in `.env`

2. **Monitor Logs**
   - Check `logs/pipeline.log` regularly
   - Look for errors and warnings

3. **Use Examples**
   - Start with simple examples
   - Modify them for your needs

4. **Follow the Pattern**
   - Collectors collect data
   - Storage stores data
   - Config controls behavior
   - Logs record everything

## Troubleshooting

1. **Configuration Issues**
   - Check YAML syntax
   - Verify file paths

2. **Collection Errors**
   - Check API keys
   - Verify URLs
   - Check internet connection

3. **Storage Problems**
   - Verify Google Cloud credentials
   - Check permissions
   - Monitor storage space

## Next Steps

1. **Start Small**
   - Run simple examples
   - Check the logs
   - Understand the flow

2. **Experiment**
   - Modify configurations
   - Try different collectors
   - Test storage options

3. **Build Your Own**
   - Add new collectors
   - Customize storage
   - Extend functionality

Remember: This is a learning process. Start with the examples, understand each component, and gradually build up to more complex uses. 