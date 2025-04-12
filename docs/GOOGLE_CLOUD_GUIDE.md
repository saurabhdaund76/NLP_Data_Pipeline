# Google Cloud Storage Guide

## Table of Contents
1. [Initial Setup](#1-initial-setup)
2. [Project Configuration](#2-project-configuration)
3. [Storage Setup](#3-storage-setup)
4. [Authentication](#4-authentication)
5. [Using Cloud Storage](#5-using-cloud-storage)
6. [Best Practices](#6-best-practices)
7. [Troubleshooting](#7-troubleshooting)

## 1. Initial Setup

### 1.1 Create Google Cloud Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Sign In" or "Get Started for Free"
3. Sign in with your Google account or create one
4. Set up billing (required for using services)

### 1.2 Install Google Cloud SDK
```bash
# For macOS (using Homebrew)
brew install google-cloud-sdk

# For Ubuntu/Debian
# Add the Cloud SDK distribution URI as a package source
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update and install the SDK
sudo apt-get update && sudo apt-get install google-cloud-sdk

# For Windows
# Download the installer from: https://cloud.google.com/sdk/docs/install-sdk#windows
```

### 1.3 Initialize SDK
```bash
# Initialize the SDK
gcloud init

# Login to your account
gcloud auth login

# Set your project
gcloud config set project your-project-id
```

## 2. Project Configuration

### 2.1 Create New Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click "New Project"
4. Enter project details:
   - Name: `nlp-data-pipeline` (or your preferred name)
   - Organization: Select if applicable
   - Location: Select if applicable
5. Click "Create"

### 2.2 Enable Required APIs
1. Go to [APIs & Services > Library](https://console.cloud.google.com/apis/library)
2. Search for and enable:
   - Cloud Storage API
   - Cloud Storage JSON API
   - Cloud Build API (if using CI/CD)

## 3. Storage Setup

### 3.1 Create Storage Bucket
1. Go to [Cloud Storage > Browser](https://console.cloud.google.com/storage/browser)
2. Click "Create Bucket"
3. Configure bucket:
   ```
   Name: your-unique-bucket-name
   Location: Choose based on your needs
   Storage class: Standard
   Access control: Uniform
   Protection tools: None (or configure as needed)
   ```
4. Click "Create"

### 3.2 Configure Bucket Permissions
1. Select your bucket
2. Go to "Permissions" tab
3. Click "Add Members"
4. Add service account or users
5. Assign roles:
   - Storage Object Viewer (read)
   - Storage Object Creator (write)
   - Storage Object Admin (full control)

## 4. Authentication

### 4.1 Create Service Account
1. Go to [IAM & Admin > Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Click "Create Service Account"
3. Enter details:
   ```
   Name: nlp-pipeline-sa
   Description: Service account for NLP Data Pipeline
   ```
4. Assign roles:
   - Storage Object Admin
   - (Add other roles as needed)
5. Click "Done"

### 4.2 Generate Credentials
1. Find your service account in the list
2. Click on the email address
3. Go to "Keys" tab
4. Click "Add Key" > "Create New Key"
5. Choose JSON format
6. Download the key file

### 4.3 Secure Credentials
1. Rename the downloaded file to `service-account.json`
2. Move it to your project's root (it will be ignored by git)
3. Add to `.env`:
```env
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_BUCKET=your-bucket-name
```

## 5. Using Cloud Storage

### 5.1 Python Setup
```bash
# Install required packages
pip install google-cloud-storage

# Verify installation
python -c "from google.cloud import storage"
```

### 5.2 Basic Usage
```python
from google.cloud import storage

# Initialize client
storage_client = storage.Client()

# Get bucket
bucket = storage_client.bucket('your-bucket-name')

# Upload file
blob = bucket.blob('path/to/destination.txt')
blob.upload_from_filename('path/to/local/file.txt')

# Download file
blob = bucket.blob('path/to/cloud/file.txt')
blob.download_to_filename('path/to/local/destination.txt')
```

### 5.3 Example Implementation
```python
from google.cloud import storage
from datetime import datetime

class CloudStorage:
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
    
    def upload_file(self, source_file, destination_blob):
        blob = self.bucket.blob(destination_blob)
        blob.upload_from_filename(source_file)
        
    def download_file(self, source_blob, destination_file):
        blob = self.bucket.blob(source_blob)
        blob.download_to_filename(destination_file)
```

## 6. Best Practices

### 6.1 Security
- Never commit service account keys
- Use environment variables for configuration
- Set appropriate IAM roles
- Regularly rotate service account keys

### 6.2 Organization
```plaintext
bucket/
├── raw/              # Raw collected data
│   ├── news/
│   └── documents/
├── processed/        # Processed data
│   ├── cleaned/
│   └── analyzed/
└── metadata/        # Data about data
```

### 6.3 Naming Conventions
```python
# File naming pattern
f"{data_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"

# Example: news_20240315_143022.json
```

### 6.4 Error Handling
```python
from google.cloud import exceptions

try:
    blob.upload_from_filename(source_file)
except exceptions.NotFound:
    print(f"Bucket {bucket_name} not found")
except exceptions.Forbidden:
    print("Permission denied")
```

## 7. Troubleshooting

### 7.1 Common Issues

1. **Authentication Errors**
```bash
# Check credentials
echo $GOOGLE_APPLICATION_CREDENTIALS

# Verify authentication
gcloud auth application-default print-access-token
```

2. **Permission Issues**
- Verify IAM roles
- Check bucket permissions
- Ensure service account has necessary access

3. **Quota Limits**
- Monitor usage in Cloud Console
- Request quota increases if needed
- Implement rate limiting

### 7.2 Debugging Tips
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check bucket existence
bucket = storage_client.bucket(bucket_name)
print(f"Bucket exists: {bucket.exists()}")

# List all buckets
buckets = storage_client.list_buckets()
for bucket in buckets:
    print(bucket.name)
```

### 7.3 Useful Commands
```bash
# List buckets
gsutil ls

# Copy files
gsutil cp local_file.txt gs://bucket-name/path/

# View file
gsutil cat gs://bucket-name/path/file.txt

# Check permissions
gsutil iam get gs://bucket-name/
```

## 8. Cost Management

### 8.1 Monitoring
1. Go to [Billing > Cost Table](https://console.cloud.google.com/billing)
2. Set up budget alerts
3. Monitor storage usage

### 8.2 Optimization
- Use appropriate storage classes
- Set object lifecycle policies
- Clean up unused resources
- Implement data retention policies

### 8.3 Cost Estimation
Use the [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator) to estimate costs:
1. Select "Storage"
2. Enter estimated usage
3. Choose storage class
4. Add network usage if applicable 