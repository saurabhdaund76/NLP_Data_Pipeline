from google.cloud import storage
import json
import os
from datetime import datetime
from dotenv import load_dotenv

def store_news_data(data, source_name):
    """Store news data in GCS bucket."""
    # Load environment variables
    load_dotenv()
    
    # Initialize GCS client
    client = storage.Client()
    bucket_name = os.getenv('GCP_BUCKET_NAME')
    bucket = client.bucket(bucket_name)
    
    # Create a unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"news_data/{source_name}/{timestamp}.json"
    
    # Create blob and upload
    blob = bucket.blob(filename)
    blob.upload_from_string(
        json.dumps(data, indent=2, ensure_ascii=False),
        content_type='application/json'
    )
    
    print(f"Data stored in GCS: gs://{bucket_name}/{filename}")
    return True

def store_pdf(pdf_path, source_name):
    """Store PDF in GCS bucket."""
    # Load environment variables
    load_dotenv()
    
    # Initialize GCS client
    client = storage.Client()
    bucket_name = os.getenv('GCP_BUCKET_NAME')
    bucket = client.bucket(bucket_name)
    
    # Create a unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"pdfs/{source_name}/{timestamp}.pdf"
    
    # Upload PDF
    blob = bucket.blob(filename)
    blob.upload_from_filename(pdf_path)
    
    print(f"PDF stored in GCS: gs://{bucket_name}/{filename}")
    return True

def main():
    # Example 1: Store news data
    news_data = {
        "title": "Sample News Article",
        "content": "This is a sample news article.",
        "source": "BBC",
        "url": "https://www.bbc.com/news/sample",
        "collected_at": datetime.now().isoformat()
    }
    
    store_news_data(news_data, "bbc_news")
    
    # Example 2: Store PDF
    # Assuming you have a PDF file
    pdf_path = "sample.pdf"  # Replace with actual PDF path
    if os.path.exists(pdf_path):
        store_pdf(pdf_path, "government_reports")

if __name__ == "__main__":
    main() 