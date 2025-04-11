from google.cloud import storage
import json
from datetime import datetime

def upload_to_gcs():
    """A simple function to upload data to Google Cloud Storage."""
    print("Step 1: Initializing Google Cloud Storage client...")
    
    # Step 1: Initialize the client
    # Note: Make sure you have set up your Google Cloud credentials
    # Either set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # Or run: gcloud auth application-default login
    client = storage.Client()
    
    print("Step 2: Getting the bucket...")
    # Step 2: Get the bucket
    bucket_name = "your-bucket-name"  # Replace with your bucket name
    bucket = client.bucket(bucket_name)
    
    print("Step 3: Creating sample data...")
    # Step 3: Create some sample data
    sample_data = {
        'title': 'Sample News Article',
        'content': 'This is a sample news article for demonstration.',
        'timestamp': datetime.now().isoformat()
    }
    
    print("Step 4: Uploading to GCS...")
    # Step 4: Upload to GCS
    # Create a unique filename using timestamp
    filename = f"news_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    blob = bucket.blob(filename)
    
    # Upload the data
    blob.upload_from_string(
        json.dumps(sample_data, indent=2),
        content_type='application/json'
    )
    
    print(f"Step 5: Done! File uploaded to: gs://{bucket_name}/{filename}")
    print("You can view this file in the Google Cloud Console!")

if __name__ == "__main__":
    upload_to_gcs() 