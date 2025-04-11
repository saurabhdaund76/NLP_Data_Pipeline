from typing import Any, Dict, Optional
from datetime import datetime
import aiohttp
import PyPDF2
import io
from ..base import BaseCollector
import os
import requests
from PyPDF2 import PdfReader
import logging
from google.cloud import storage

class PDFCollector(BaseCollector):
    """Collector for PDF documents.
    
    This collector demonstrates how to:
    1. Download PDF files from URLs
    2. Extract text from PDFs
    3. Handle different PDF formats
    4. Process large PDFs efficiently
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.session: Optional[aiohttp.ClientSession] = None
        self.max_pages = config.get('max_pages', 100)  # Limit pages to process
        self.headers = {
            'User-Agent': 'NLP-Data-Pipeline/1.0'
        }
        self.storage_client = storage.Client()
        self.bucket_name = config.get('bucket_name')
        self.bucket = self.storage_client.bucket(self.bucket_name)
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self):
        """Initialize the HTTP session when entering the context."""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up the HTTP session when exiting the context."""
        if self.session:
            await self.session.close()

    async def _download_pdf(self, url: str) -> Optional[bytes]:
        """Download PDF file from URL.
        
        Args:
            url: URL of the PDF file
            
        Returns:
            PDF content as bytes, or None if download failed
        """
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                return None
        except Exception as e:
            print(f"Error downloading PDF from {url}: {str(e)}")
            return None

    def _extract_text(self, pdf_content: bytes) -> Dict[str, Any]:
        """Extract text from PDF content.
        
        Args:
            pdf_content: PDF file content as bytes
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract metadata
            metadata = pdf_reader.metadata or {}
            
            # Extract text from pages
            text_pages = []
            for i, page in enumerate(pdf_reader.pages):
                if i >= self.max_pages:
                    break
                text_pages.append(page.extract_text())
            
            return {
                'text': '\n\n'.join(text_pages),
                'metadata': {
                    'num_pages': len(pdf_reader.pages),
                    'author': metadata.get('/Author', 'Unknown'),
                    'title': metadata.get('/Title', 'Unknown'),
                    'creation_date': metadata.get('/CreationDate', 'Unknown')
                }
            }
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return None

    async def collect(self) -> Dict[str, Any]:
        """Collect and process PDF document.
        
        Steps:
        1. Download PDF
        2. Extract text and metadata
        3. Package results
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context manager.")

        try:
            # Get PDF URL from config
            pdf_url = self.config.get('url')
            if not pdf_url:
                raise ValueError("PDF URL not provided in config")

            # Step 1: Download PDF
            pdf_content = await self._download_pdf(pdf_url)
            if not pdf_content:
                self.update_stats(successful=False)
                return {
                    'data': None,
                    'metadata': {
                        'source': pdf_url,
                        'collected_at': datetime.now().isoformat(),
                        'status': 'error',
                        'error': 'Failed to download PDF'
                    }
                }

            # Step 2: Extract text and metadata
            extracted_data = self._extract_text(pdf_content)
            if not extracted_data:
                self.update_stats(successful=False)
                return {
                    'data': None,
                    'metadata': {
                        'source': pdf_url,
                        'collected_at': datetime.now().isoformat(),
                        'status': 'error',
                        'error': 'Failed to extract text from PDF'
                    }
                }

            # Step 3: Package results
            self.update_stats(successful=True)
            return {
                'data': extracted_data,
                'metadata': {
                    'source': pdf_url,
                    'collected_at': datetime.now().isoformat(),
                    'status': 'success',
                    'data_type': 'pdf_document',
                    'extraction_method': 'pdf_parser'
                }
            }

        except Exception as e:
            self.update_stats(successful=False)
            return {
                'data': None,
                'metadata': {
                    'source': self.config.get('url', 'unknown'),
                    'collected_at': datetime.now().isoformat(),
                    'status': 'error',
                    'error': str(e)
                }
            }

    async def validate(self, data: Dict[str, Any]) -> bool:
        """Validate the extracted PDF data.
        
        Checks if text was successfully extracted.
        """
        if not data or 'data' not in data:
            return False
            
        extracted_data = data['data']
        return (
            'text' in extracted_data and 
            extracted_data['text'] and 
            len(extracted_data['text'].strip()) > 0
        )

    def download_pdf(self, url):
        """Download PDF from URL."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Create a temporary file
            temp_file = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return temp_file
        except Exception as e:
            self.logger.error(f"Error downloading PDF: {str(e)}")
            return None
            
    def extract_text(self, pdf_path):
        """Extract text from PDF file."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
                
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {str(e)}")
            return None
            
    def store_pdf(self, pdf_path, source_name):
        """Store PDF in GCS bucket."""
        try:
            # Create a unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"pdfs/{source_name}/{timestamp}.pdf"
            
            # Upload to GCS
            blob = self.bucket.blob(filename)
            blob.upload_from_filename(pdf_path)
            
            # Clean up temporary file
            os.remove(pdf_path)
            
            self.logger.info(f"PDF stored in GCS: gs://{self.bucket_name}/{filename}")
            return True
        except Exception as e:
            self.logger.error(f"Error storing PDF: {str(e)}")
            return False
            
    def process_pdf(self, url, source_name):
        """Process PDF from URL: download, extract text, and store."""
        try:
            # Download PDF
            pdf_path = self.download_pdf(url)
            if not pdf_path:
                return None
                
            # Extract text
            text = self.extract_text(pdf_path)
            if not text:
                return None
                
            # Store PDF
            if not self.store_pdf(pdf_path, source_name):
                return None
                
            return {
                'url': url,
                'text': text,
                'source': source_name,
                'collected_at': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error processing PDF: {str(e)}")
            return None 