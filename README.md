# NLP Data Pipeline

A production-ready data pipeline for collecting, processing, and storing NLP data from various sources.

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/username/nlp-data-pipeline.git
cd nlp-data-pipeline
```

2. Set up virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Documentation

### Setup Guides
- [Git Guide](docs/GIT_GUIDE.md) - Complete guide for Git setup and usage
- [Google Cloud Guide](docs/GOOGLE_CLOUD_GUIDE.md) - Detailed instructions for Google Cloud Storage setup

### Project Documentation
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Overview of project organization
- [API Reference](docs/API_REFERENCE.md) - API documentation
- [Architecture](docs/ARCHITECTURE.md) - System architecture details

## Features

- Multiple data sources support:
  - Web scraping
  - News APIs
  - PDF documents
  
- Flexible storage options:
  - Local file system
  - Google Cloud Storage
  
- Data processing:
  - Text cleaning
  - NLP processing
  - Data transformation

## Storage Options

### Local Storage
- File-based storage
- Multiple formats (JSON, CSV, Pickle)
- Organized directory structure

### Google Cloud Storage
- Cloud-based storage
- Scalable and secure
- Automated backups

## Configuration

The project uses both `.env` files and YAML configurations:

1. Environment Variables (`.env`):
```env
NEWS_API_KEY=your_key
GOOGLE_CLOUD_KEY=your_key
```

2. YAML Configurations:
```yaml
storage:
  local:
    base_path: "./data"
  cloud:
    bucket: "your-bucket"
```

## Development

### Prerequisites
- Python 3.8+
- Git
- Google Cloud SDK (for cloud storage)

### Setting Up Development Environment
1. Follow the [Git Guide](docs/GIT_GUIDE.md)
2. Set up cloud storage using [Google Cloud Guide](docs/GOOGLE_CLOUD_GUIDE.md)
3. Install dependencies
4. Configure environment variables

### Running Tests
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

See [Git Guide](docs/GIT_GUIDE.md) for detailed instructions.

## Security

- Never commit sensitive data
- Use environment variables for secrets
- Follow security best practices in [Google Cloud Guide](docs/GOOGLE_CLOUD_GUIDE.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
- Create an issue for bug reports or feature requests
- Submit PRs for any improvements 