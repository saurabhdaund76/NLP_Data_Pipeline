import os
from google.cloud import storage
import requests
from dotenv import load_dotenv

def test_gcs_connection():
    """Test Google Cloud Storage connection."""
    try:
        # Initialize client
        client = storage.Client()
        bucket_name = os.getenv('GCP_BUCKET_NAME')
        bucket = client.bucket(bucket_name)
        
        # Test bucket access
        if bucket.exists():
            print("✅ Successfully connected to GCS bucket")
            return True
        else:
            print("❌ Failed to access GCS bucket")
            return False
    except Exception as e:
        print(f"❌ GCS Error: {str(e)}")
        return False

def test_news_api():
    """Test News API connection."""
    try:
        api_key = os.getenv('NEWS_API_KEY')
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Successfully connected to News API")
            return True
        else:
            print(f"❌ News API Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ News API Error: {str(e)}")
        return False

def main():
    # Load environment variables
    load_dotenv()
    
    print("Testing setup...\n")
    
    # Test GCS connection
    print("Testing Google Cloud Storage connection...")
    gcs_success = test_gcs_connection()
    
    # Test News API connection
    print("\nTesting News API connection...")
    api_success = test_news_api()
    
    # Print summary
    print("\nSetup Test Summary:")
    print(f"Google Cloud Storage: {'✅' if gcs_success else '❌'}")
    print(f"News API: {'✅' if api_success else '❌'}")
    
    if gcs_success and api_success:
        print("\n🎉 All tests passed! Your setup is ready to use.")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 