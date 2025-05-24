# Migration Guide: Legacy to Modular Structure

This guide helps you migrate from the old flat structure to the new professional modular structure.

## 🔄 What Changed

### Old Structure
```
google-image-scraper-clean/
├── GoogleImageScraper.py    # Monolithic scraper
├── config.py               # Configuration
├── exceptions.py           # Exceptions
├── utils.py               # Utilities
├── logger_utils.py        # Logging
├── cli.py                 # CLI
├── example.py             # Examples
└── main.py                # Main script
```

### New Structure
```
google-image-scraper-clean/
├── src/
│   └── google_image_scraper/
│       ├── __init__.py
│       ├── core/
│       │   ├── scraper.py
│       │   ├── config.py
│       │   └── exceptions.py
│       ├── utils/
│       │   ├── helpers.py
│       │   └── logging.py
│       └── cli/
│           └── main.py
├── examples/
└── docs/
```

## 📦 Import Changes

### Old Imports
```python
# Old way
from GoogleImageScraper import find_image_urls, save_images
from config import DEFAULT_CONFIG, ScrapingConfig
from exceptions import BrowserError, ImageDownloadError
from utils import decode_url, clean_search_key
from logger_utils import setup_logger
```

### New Imports
```python
# New way - Main package imports
from google_image_scraper import GoogleImageScraper, ScrapingConfig, DEFAULT_CONFIG
from google_image_scraper import BrowserError, ImageDownloadError

# Or specific module imports
from google_image_scraper.core.scraper import GoogleImageScraper
from google_image_scraper.core.config import ScrapingConfig
from google_image_scraper.core.exceptions import BrowserError
from google_image_scraper.utils.helpers import decode_url, clean_search_key
from google_image_scraper.utils.logging import setup_logger
```

## 🔧 API Changes

### Old Function-Based API
```python
# Old way
import asyncio
from GoogleImageScraper import find_image_urls, save_images

async def old_way():
    # Extract URLs
    urls = await find_image_urls(
        search_key='cats',
        number_of_images=10,
        headless=True
    )
    
    # Save images
    await save_images(
        image_urls=urls,
        images_dir_path='photos',
        image_file_prefix='cat'
    )

asyncio.run(old_way())
```

### New Class-Based API
```python
# New way
import asyncio
from google_image_scraper import GoogleImageScraper, ScrapingConfig

async def new_way():
    # Create scraper with configuration
    config = ScrapingConfig(
        number_of_images=10,
        headless=True,
        photos_dir='photos'
    )
    scraper = GoogleImageScraper(config)
    
    # Complete workflow (extract + download)
    urls, downloaded_count = await scraper.scrape('cats')
    
    # Or just extract URLs
    urls = await scraper.find_image_urls('cats')
    
    # Or just download from URLs
    downloaded_count = await scraper.save_images(urls, 'cats')

asyncio.run(new_way())
```

## 🖥️ CLI Changes

### Old CLI Usage
```bash
# Old way
python cli.py cats dogs --count 10 --headless
```

### New CLI Usage
```bash
# New way - installed package
google-image-scraper cats dogs --count 10 --headless

# Or short alias
gis cats dogs --count 10 --headless

# Or as module
python -m google_image_scraper cats dogs --count 10 --headless
```

## ⚙️ Configuration Changes

### Old Configuration
```python
# Old way
from config import ScrapingConfig

config = ScrapingConfig()
config.number_of_images = 20
config.headless = True
```

### New Configuration
```python
# New way - same interface, better imports
from google_image_scraper import ScrapingConfig

config = ScrapingConfig(
    number_of_images=20,
    headless=True
)
```

## 🔄 Step-by-Step Migration

### 1. Update Imports
Replace all old imports with new package imports:

```python
# Replace this:
from GoogleImageScraper import find_image_urls, save_images
from config import ScrapingConfig

# With this:
from google_image_scraper import GoogleImageScraper, ScrapingConfig
```

### 2. Update Function Calls to Class Methods
Replace function calls with class-based API:

```python
# Old:
urls = await find_image_urls('cats', 10, True)
await save_images(urls, 'jpg', 'photos', False, 'cat')

# New:
scraper = GoogleImageScraper()
urls, count = await scraper.scrape('cats')
```

### 3. Update Configuration Usage
Configuration API remains the same, just import path changed:

```python
# Old:
from config import ScrapingConfig, DEFAULT_CONFIG

# New:
from google_image_scraper import ScrapingConfig, DEFAULT_CONFIG
```

### 4. Update CLI Scripts
Replace direct script calls with package commands:

```bash
# Old:
python cli.py search_term

# New:
google-image-scraper search_term
```

### 5. Update Exception Handling
Exception names and usage remain the same:

```python
# Old:
from exceptions import BrowserError, ImageDownloadError

# New:
from google_image_scraper import BrowserError, ImageDownloadError
```

## 🧪 Testing Your Migration

### 1. Test Basic Import
```python
try:
    from google_image_scraper import GoogleImageScraper
    print("✅ Import successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
```

### 2. Test Basic Functionality
```python
import asyncio
from google_image_scraper import GoogleImageScraper

async def test():
    scraper = GoogleImageScraper()
    urls = await scraper.find_image_urls('test')
    print(f"✅ Found {len(urls)} URLs")

asyncio.run(test())
```

### 3. Test CLI
```bash
google-image-scraper --help
```

## 🚨 Breaking Changes

### 1. Import Paths
All import paths have changed. Use the new package structure.

### 2. API Design
Moved from function-based to class-based API for better organization.

### 3. CLI Command
CLI is now a proper package command instead of a script.

### 4. File Organization
Source code is now in `src/` directory following Python packaging best practices.

## 🔄 Backwards Compatibility

To maintain backwards compatibility temporarily, you could create wrapper functions:

```python
# compatibility.py - temporary bridge
from google_image_scraper import GoogleImageScraper, ScrapingConfig

# Global scraper instance for backwards compatibility
_default_scraper = GoogleImageScraper()

async def find_image_urls(search_key, number_of_images=10, max_missed=10, headless=True):
    """Backwards compatibility wrapper"""
    config = ScrapingConfig(
        number_of_images=number_of_images,
        max_missed=max_missed,
        headless=headless
    )
    scraper = GoogleImageScraper(config)
    return await scraper.find_image_urls(search_key)

async def save_images(image_urls, image_save_format='jpg', images_dir_path='photos', 
                     keep_filenames=False, image_file_prefix='image',
                     min_resolution=(0, 0), max_resolution=(9999, 9999)):
    """Backwards compatibility wrapper"""
    # Implementation using new API
    pass
```

## 🎯 Benefits of New Structure

1. **Professional Package Structure**: Follows Python packaging best practices
2. **Better Modularity**: Clear separation of concerns
3. **Type Safety**: Full type annotations for better IDE support
4. **CLI Integration**: Proper entry points for command-line usage
5. **Extensibility**: Easier to extend and maintain
6. **Testing**: Better structure for unit testing
7. **Documentation**: Organized documentation and examples

## 📞 Need Help?

If you encounter issues during migration:

1. Check the [API Reference](API.md)
2. Look at [examples/basic_usage.py](../examples/basic_usage.py)
3. Open an issue on GitHub
4. Check the migration examples above
