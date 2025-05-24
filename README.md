# Google Image Scraper with Playwright

A robust Python script to scrape and download full-resolution images from Google Images using Playwright with advanced features including performance monitoring, comprehensive logging, and CLI interface.

## ✨ Features

- ✅ **Full-resolution image extraction** - Gets actual high-quality images, not thumbnails
- ✅ **JSON URL saving** - Saves all extracted URLs to timestamped JSON files
- ✅ **Advanced URL filtering** - Filters out thumbnails, logos, and low-quality images
- ✅ **Parallel processing** - Supports multiple search terms simultaneously
- ✅ **Robust error handling** - Continues working even if some images fail to download
- ✅ **Browser automation** - Uses Playwright for reliable web scraping
- ✅ **Performance monitoring** - Track memory usage, CPU usage, and download rates
- ✅ **Comprehensive logging** - Detailed logs with different verbosity levels
- ✅ **CLI interface** - Easy-to-use command line interface
- ✅ **Input validation** - Validates all inputs to prevent errors
- ✅ **Configuration management** - Centralized configuration system
- ✅ **Type hints** - Full type annotations for better code quality

## 🚀 Quick Start

### Installation

1. **Clone or download this project**

2. **Run the setup script:**
   ```bash
   python setup.py
   ```
   
   Or install manually:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

### Basic Usage

#### Using the CLI (Recommended)
```bash
# Basic usage
python cli.py cats dogs --count 10

# Advanced usage with options
python cli.py "red roses" --count 20 --min-res 800x600 --max-res 1920x1080 --headless

# Dry run (extract URLs but don't download)
python cli.py "python programming" --dry-run --verbose
```

#### Using the Python API
```python
import asyncio
from GoogleImageScraper import find_image_urls, save_images

async def scrape_images():
    # Find image URLs
    urls = await find_image_urls(
        search_key='cats',
        number_of_images=10,
        headless=True
    )
    
    # Download images
    if urls:
        await save_images(
            image_urls=urls,
            images_dir_path='my_photos',
            image_file_prefix='cat'
        )

asyncio.run(scrape_images())
```

## 📖 Detailed Documentation

### Command Line Interface

The CLI provides the most user-friendly way to use the scraper:

```bash
python cli.py [search_terms] [options]
```

**Positional Arguments:**
- `search_terms`: One or more search terms to scrape images for

**Options:**
- `-c, --count`: Number of images per search term (default: 10)
- `--max-missed`: Max failed downloads before stopping (default: 10)
- `--headless`: Run browser without GUI
- `--show-browser`: Show browser GUI
- `--min-res`: Minimum resolution (e.g., 800x600)
- `--max-res`: Maximum resolution (e.g., 1920x1080)
- `--format`: Image format (jpg, png, jpeg)
- `--output`: Output directory (default: photos)
- `--keep-filenames`: Keep original URL filenames
- `--timeout`: Download timeout in seconds
- `--workers`: Number of concurrent workers
- `--verbose`: Enable verbose logging
- `--dry-run`: Extract URLs but don't download

**Examples:**
```bash
# Download 20 cat images in headless mode
python cli.py cats --count 20 --headless

# Download high-resolution rose images
python cli.py "red roses" --min-res 1024x768 --max-res 2560x1440

# Multiple search terms with custom output
python cli.py cats dogs birds --output ./animals --format png

# Dry run to see what would be downloaded
python cli.py "vintage cars" --dry-run --verbose
```
    # Extract URLs
    image_urls = await find_image_urls(
        search_key='cat',
        number_of_images=10,
        headless=True
    )
    
    # Download images
    await save_images(
        image_urls=image_urls,
        images_dir_path='my_photos',
        image_file_prefix='cat'
    )

asyncio.run(scrape_images())
```

### Configuration

Modify these parameters in `main.py`:

```python
number_of_images = 10                # Number of images to download
min_resolution = (0, 0)             # Minimum image resolution
max_resolution = (9999, 9999)       # Maximum image resolution
headless = True                     # Run browser in background
```

## Output Structure

```
project/
├── photos/                    # Downloaded images
│   ├── cat/
│   │   ├── cat-0.jpg
│   │   ├── cat-1.jpg
│   │   └── ...
│   └── dog/
│       ├── dog-0.jpg
│       └── ...
└── google_search/            # JSON files with URLs
    ├── cat_20250524_143022.json
    ├── dog_20250524_143055.json
    └── ...
```

## JSON Output Format

Each search creates a JSON file with extracted URLs:

```json
{
  "search_key": "cat",
  "timestamp": "2025-05-24T14:30:22.123456",
  "total_urls": 10,
  "image_urls": [
    "https://example.com/full-resolution-image1.jpg",
    "https://example.com/full-resolution-image2.jpg"
  ]
}
```

## Requirements

- Python 3.7+
- playwright
- httpx
- Pillow (PIL)

## How It Works

1. **URL Extraction**: Uses multiple methods to extract full-resolution image URLs:
   - Analyzes JavaScript data in Google Images page
   - Scans meta tags and page content
   - Optionally clicks on images to get full-size versions

2. **Quality Filtering**: Filters out:
   - Encrypted thumbnails (`encrypted-tbn`)
   - Small image indicators (`s64`, `s90`, `s100`)
   - Logo and favicon images
   - Very short URLs (likely thumbnails)

3. **URL Cleaning**: Properly decodes Unicode escapes and URL encoding

4. **Download**: Downloads images with proper error handling and timeout management

## Notes

- Some images may fail to download due to anti-bot protection or 404 errors - this is normal
- The script respects rate limits and includes delays to avoid being blocked
- Full-resolution images are much larger than thumbnails (typically 500KB - 5MB vs 5-50KB)
- JSON files allow you to reuse URLs without re-scraping

## Troubleshooting

**Issue**: No images downloaded
- Check your internet connection
- Try running with `headless=False` to see browser activity
- Some searches may have limited high-quality images available

**Issue**: Low image quality
- The script now extracts full-resolution URLs by default
- Check the JSON files to verify URL quality
- Some search terms may have fewer high-quality images available

**Issue**: Browser errors
- Run `playwright install` to ensure browsers are installed
- Try updating Playwright: `pip install --upgrade playwright`
