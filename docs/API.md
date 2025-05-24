# API Reference

## Core Classes

### GoogleImageScraper

The main scraper class that provides the interface for scraping Google Images.

```python
from google_image_scraper import GoogleImageScraper, ScrapingConfig

# Create with default configuration
scraper = GoogleImageScraper()

# Create with custom configuration
config = ScrapingConfig(number_of_images=20, headless=True)
scraper = GoogleImageScraper(config)
```

#### Methods

##### `async scrape(search_key: str) -> Tuple[List[str], int]`

Complete scraping workflow: find URLs and download images.

**Parameters:**
- `search_key` (str): The search term to use

**Returns:**
- Tuple of (image_urls, downloaded_count)

**Example:**
```python
urls, count = await scraper.scrape('cats')
print(f"Downloaded {count} images from {len(urls)} URLs")
```

##### `async find_image_urls(search_key: str) -> List[str]`

Search and return image URLs without downloading.

**Parameters:**
- `search_key` (str): The search term to use

**Returns:**
- List of image URLs

**Example:**
```python
urls = await scraper.find_image_urls('dogs')
print(f"Found {len(urls)} URLs")
```

##### `async save_images(image_urls: List[str], search_key: str) -> int`

Download images from URLs to the configured directory.

**Parameters:**
- `image_urls` (List[str]): List of image URLs to download
- `search_key` (str): Search term used (for directory naming)

**Returns:**
- Number of successfully downloaded images

### ScrapingConfig

Configuration class for customizing scraper behavior.

```python
from google_image_scraper import ScrapingConfig

config = ScrapingConfig(
    number_of_images=10,
    headless=True,
    min_resolution=(800, 600),
    max_resolution=(1920, 1080),
    image_save_format='png'
)
```

#### Parameters

- `number_of_images` (int): Number of images to download (default: 10)
- `max_missed` (int): Maximum failed downloads before stopping (default: 10)
- `headless` (bool): Run browser in headless mode (default: True)
- `min_resolution` (Tuple[int, int]): Minimum image resolution (default: (0, 0))
- `max_resolution` (Tuple[int, int]): Maximum image resolution (default: (9999, 9999))
- `keep_filenames` (bool): Keep original filenames from URLs (default: False)
- `image_save_format` (str): Image save format: 'jpg', 'png', 'jpeg' (default: 'jpg')
- `timeout_seconds` (float): Download timeout in seconds (default: 5.0)
- `scroll_attempts` (int): Number of scroll attempts on the page (default: 3)
- `click_timeout` (int): Click timeout in milliseconds (default: 3000)
- `photos_dir` (str): Output directory for images (default: 'photos')
- `json_dir` (str): Directory for JSON metadata files (default: 'google_search')

## Exceptions

### GoogleImageScraperError

Base exception for all scraper-related errors.

### BrowserError

Raised when browser operations fail.

### ImageDownloadError

Raised when image download fails.

**Attributes:**
- `url` (str): The URL that failed to download
- `reason` (str): The reason for failure

### InvalidResolutionError

Raised when image resolution doesn't meet criteria.

**Attributes:**
- `actual_resolution` (tuple): The actual image resolution
- `min_resolution` (tuple): The minimum allowed resolution
- `max_resolution` (tuple): The maximum allowed resolution

### URLExtractionError

Raised when URL extraction fails.

### FileOperationError

Raised when file operations fail.

**Attributes:**
- `operation` (str): The operation that failed (e.g., "save", "create")
- `path` (str): The file path involved
- `reason` (str): The reason for failure

## Utility Functions

### Helper Functions

Available in `google_image_scraper.utils.helpers`:

#### `is_valid_image_url(url: str) -> bool`

Check if a URL points to a valid image.

#### `clean_search_key(search_key: str) -> str`

Clean and normalize search key for use in filenames.

#### `decode_url(url: str) -> str`

Decode URL-encoded characters and unicode escapes.

#### `filter_thumbnail_urls(urls: List[str], thumbnail_patterns: List[str]) -> List[str]`

Filter out thumbnail and low-quality image URLs.

#### `validate_resolution(width: int, height: int, min_resolution: Tuple[int, int], max_resolution: Tuple[int, int]) -> bool`

Check if image resolution is within specified bounds.

### Logging Functions

Available in `google_image_scraper.utils.logging`:

#### `setup_logger(name: str = "GoogleImageScraper", level: int = logging.INFO) -> logging.Logger`

Set up a logger with both file and console handlers.

#### `log_scraping_summary(logger: logging.Logger, search_key: str, found_urls: int, downloaded_images: int, failed_downloads: int)`

Log a summary of the scraping results.
