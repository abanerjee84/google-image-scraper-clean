# Google Image Scraper - Professional Edition

A sophisticated, modular Python package for scraping and downloading high-resolution images from Google Images with advanced filtering, error handling, and professional code structure.

## 🌟 Features

- **Full-Resolution Images**: Advanced extraction methods to get actual full-size images, not thumbnails
- **Professional Architecture**: Clean, modular codebase with proper separation of concerns
- **Async/Await Support**: High-performance asynchronous operations
- **Advanced Filtering**: Resolution-based filtering, thumbnail detection, and quality control
- **Robust Error Handling**: Comprehensive exception handling with detailed logging
- **CLI Interface**: Feature-rich command-line interface with extensive options
- **Configurable**: Highly customizable configuration system
- **Type Hints**: Full type annotation support for better IDE integration
- **Comprehensive Logging**: Detailed logging with file and console output

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Installation
```bash
# Clone the repository
git clone https://github.com/abanerjee84/google-image-scraper-clean.git
cd google-image-scraper-clean

# Install in development mode (recommended)
pip install -e .

# Or install dependencies manually
pip install -r requirements.txt
playwright install
```

### Using the new setup script
```bash
python setup_new.py
```

## 🚀 Quick Start

### Command Line Usage

```bash
# Basic usage
google-image-scraper cats dogs --count 10

# Advanced usage with resolution filtering
google-image-scraper "red roses" --count 20 --min-res 800x600 --max-res 1920x1080 --format png

# Dry run (extract URLs only)
google-image-scraper "python programming" --dry-run --verbose

# Using short alias
gis cats --count 5 --headless
```

### Python Library Usage

```python
import asyncio
from google_image_scraper import GoogleImageScraper, ScrapingConfig

async def main():
    # Create custom configuration
    config = ScrapingConfig(
        number_of_images=10,
        headless=True,
        min_resolution=(800, 600),
        max_resolution=(1920, 1080),
        image_save_format='png',
        photos_dir='downloads'
    )
    
    # Create scraper instance
    scraper = GoogleImageScraper(config)
    
    # Scrape images (find URLs and download)
    image_urls, downloaded_count = await scraper.scrape('cats')
    print(f"Downloaded {downloaded_count} images")
    
    # Or just extract URLs without downloading
    urls = await scraper.find_image_urls('dogs')
    print(f"Found {len(urls)} URLs")

# Run the async function
asyncio.run(main())
```

## 📁 Project Structure

```
google-image-scraper-clean/
├── src/
│   └── google_image_scraper/
│       ├── __init__.py              # Package initialization
│       ├── core/                    # Core functionality
│       │   ├── __init__.py
│       │   ├── scraper.py          # Main scraper class
│       │   ├── config.py           # Configuration classes
│       │   └── exceptions.py       # Custom exceptions
│       ├── utils/                   # Utility functions
│       │   ├── __init__.py
│       │   ├── helpers.py          # Helper functions
│       │   └── logging.py          # Logging utilities
│       └── cli/                     # Command-line interface
│           ├── __init__.py
│           └── main.py             # CLI implementation
├── examples/                        # Usage examples
│   └── basic_usage.py              # Basic usage examples
├── docs/                           # Documentation
├── tests/                          # Test cases
├── requirements.txt                # Core dependencies
├── requirements-dev.txt            # Development dependencies
├── setup_new.py                   # New professional setup script
└── README.md                      # This file
```

## ⚙️ Configuration Options

The `ScrapingConfig` class provides extensive customization options:

```python
from google_image_scraper import ScrapingConfig

config = ScrapingConfig(
    number_of_images=10,           # Number of images to download
    max_missed=10,                 # Max failed downloads before stopping
    headless=True,                 # Run browser in headless mode
    min_resolution=(800, 600),     # Minimum image resolution
    max_resolution=(1920, 1080),   # Maximum image resolution
    keep_filenames=False,          # Keep original filenames
    image_save_format='jpg',       # Image format (jpg, png, jpeg)
    timeout_seconds=5.0,           # Download timeout
    scroll_attempts=3,             # Number of scroll attempts
    click_timeout=3000,            # Click timeout in milliseconds
    photos_dir='photos',           # Output directory
    json_dir='google_search',      # JSON output directory
)
```

## 🖥️ CLI Options

```bash
google-image-scraper --help

usage: google-image-scraper [-h] [-c COUNT] [--max-missed MAX_MISSED] 
                           [--headless] [--show-browser] [--min-res MIN_RES] 
                           [--max-res MAX_RES] [--format {jpg,png,jpeg}] 
                           [--output OUTPUT] [--keep-filenames] 
                           [--timeout TIMEOUT] [--verbose] [--dry-run] 
                           search_terms [search_terms ...]

Options:
  -c, --count           Number of images per search term (default: 10)
  --max-missed          Max failed downloads before stopping (default: 10)
  --headless            Run browser in headless mode
  --show-browser        Show browser GUI
  --min-res             Minimum resolution (e.g., 800x600)
  --max-res             Maximum resolution (e.g., 1920x1080)
  --format              Image format: jpg, png, jpeg (default: jpg)
  --output, -o          Output directory (default: photos)
  --keep-filenames      Keep original filenames from URLs
  --timeout             Download timeout in seconds (default: 5.0)
  --verbose, -v         Enable verbose logging
  --dry-run             Extract URLs but don't download images
```

## 📊 Examples

### Basic Example
```python
# examples/basic_usage.py
import asyncio
from google_image_scraper import GoogleImageScraper

async def simple_example():
    scraper = GoogleImageScraper()
    image_urls, downloaded = await scraper.scrape('cats')
    print(f"Downloaded {downloaded} cat images")

asyncio.run(simple_example())
```

### Advanced Example
```python
# Advanced configuration with resolution filtering
config = ScrapingConfig(
    number_of_images=20,
    min_resolution=(1024, 768),
    max_resolution=(2560, 1440),
    image_save_format='png',
    headless=True
)

scraper = GoogleImageScraper(config)
urls, count = await scraper.scrape('landscape photography')
```

## 🔧 Development

### Setting up for Development

```bash
# Clone and install in development mode
git clone https://github.com/abanerjee84/google-image-scraper-clean.git
cd google-image-scraper-clean
pip install -e .
pip install -r requirements-dev.txt
```

### Running Tests
```bash
python -m pytest tests/
```

### Code Quality
```bash
# Type checking
mypy src/

# Linting
flake8 src/

# Formatting
black src/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Please respect robots.txt files and website terms of service. Use responsibly and consider the legal implications of web scraping in your jurisdiction.

## 🔗 Links

- [GitHub Repository](https://github.com/abanerjee84/google-image-scraper-clean)
- [Issue Tracker](https://github.com/abanerjee84/google-image-scraper-clean/issues)
- [Documentation](https://github.com/abanerjee84/google-image-scraper-clean#readme)

## 📈 Roadmap

- [ ] Add support for other search engines
- [ ] Implement image deduplication
- [ ] Add batch processing capabilities
- [ ] Create web interface
- [ ] Add docker support
- [ ] Implement caching mechanisms
