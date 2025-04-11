# Hands-On Learning Guide

This guide provides practical exercises to help you understand how the NLP Data Collection Pipeline works. Follow these exercises in order.

## Exercise 1: Basic Setup and Configuration

### Goal
Set up the project and understand configuration files.

### Steps
1. **Create Virtual Environment**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install requirements
   pip install -r requirements.txt
   ```

2. **Examine Configuration**
   ```bash
   # Open config file
   cat config/news_scraper_config.yaml
   
   # Try modifying settings
   nano config/news_scraper_config.yaml
   ```

3. **Check Your Understanding**
   - What settings can you change?
   - Where are sensitive data stored?
   - How do settings affect behavior?

## Exercise 2: Collecting News Data

### Goal
Collect news articles from BBC News.

### Steps
1. **Run Simple Example**
   ```python
   # Run the example
   python examples/simple_example.py
   
   # Check the output
   cat logs/pipeline.log
   ```

2. **Modify the Example**
   ```python
   # Open example file
   nano examples/simple_example.py
   
   # Change the URL
   url = "https://www.bbc.com/news/technology"
   ```

3. **Practice Tasks**
   - Collect articles from different sections
   - Save articles to different locations
   - Handle collection errors

## Exercise 3: Working with PDFs

### Goal
Download and store PDF documents.

### Steps
1. **Run PDF Example**
   ```python
   # Run the example
   python examples/pdf_example.py
   ```

2. **Examine Storage**
   ```bash
   # List stored PDFs
   gsutil ls gs://your-bucket-name/pdfs/
   ```

3. **Practice Tasks**
   - Download different PDFs
   - Extract text content
   - Store in different formats

## Exercise 4: Using Google Cloud Storage

### Goal
Understand how cloud storage works.

### Steps
1. **Check Storage Setup**
   ```bash
   # Verify credentials
   echo $GOOGLE_APPLICATION_CREDENTIALS
   
   # List buckets
   gsutil ls
   ```

2. **Store and Retrieve**
   ```python
   # Store data
   storage.store_data(data, "test_data")
   
   # List stored files
   storage.list_files()
   ```

3. **Practice Tasks**
   - Create different storage paths
   - Manage file permissions
   - Monitor storage usage

## Exercise 5: Error Handling and Logging

### Goal
Learn how to handle errors and use logs.

### Steps
1. **Generate Errors**
   ```python
   # Try invalid URL
   scraper.scrape_article("invalid_url")
   
   # Check error logs
   tail -f logs/pipeline.log
   ```

2. **Add Custom Logging**
   ```python
   # Add log statements
   logger.info("Starting collection...")
   logger.error("Failed to collect data")
   ```

3. **Practice Tasks**
   - Handle different error types
   - Add custom log messages
   - Monitor error patterns

## Exercise 6: Building Your Own Collector

### Goal
Create a custom data collector.

### Steps
1. **Create Collector File**
   ```bash
   # Create new file
   touch src/collectors/api/custom_collector.py
   ```

2. **Implement Collector**
   ```python
   class CustomCollector:
       def __init__(self, config):
           self.config = config
           
       def collect(self):
           # Your collection logic here
           pass
   ```

3. **Practice Tasks**
   - Choose a data source
   - Implement collection logic
   - Add error handling
   - Write tests

## Exercise 7: Complete Pipeline

### Goal
Build a complete data collection pipeline.

### Steps
1. **Configure Sources**
   ```yaml
   # Add to config/news_scraper_config.yaml
   custom_source:
     url: "your_source_url"
     settings:
       key1: value1
       key2: value2
   ```

2. **Create Pipeline**
   ```python
   # Combine collectors
   collectors = [
       NewsCollector(config),
       PDFCollector(config),
       CustomCollector(config)
   ]
   
   # Run pipeline
   for collector in collectors:
       data = collector.collect()
       storage.store(data)
   ```

3. **Practice Tasks**
   - Add multiple sources
   - Implement parallel collection
   - Add monitoring
   - Handle failures

## Next Steps

1. **Advanced Topics**
   - Implement rate limiting
   - Add data validation
   - Create monitoring dashboard
   - Optimize storage

2. **Project Ideas**
   - News aggregator
   - Document archive
   - Research data collector
   - Social media analyzer

Remember:
- Start simple
- Test thoroughly
- Monitor everything
- Handle errors gracefully
- Document your changes 