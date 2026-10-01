# Google Image Scraper

A modular Python package for searching Google Images, extracting full-resolution image URLs and downloading images with configurable filtering and asynchronous processing.

The project provides both a command-line interface and a Python API.

## Features

- asynchronous scraping and download workflow;
- full-resolution image URL extraction;
- minimum and maximum resolution filtering;
- thumbnail detection and filtering;
- configurable output format and directories;
- command-line interface;
- reusable Python API;
- structured logging;
- type annotations;
- tests and usage examples.

## Project Structure

```text
google-image-scraper-clean/
├── src/
│   └── google_image_scraper/
│       ├── core/
│       │   ├── scraper.py
│       │   ├── config.py
│       │   └── exceptions.py
│       ├── utils/
│       └── cli/
├── examples/
├── docs/
├── tests/
├── requirements.txt
├── requirements-dev.txt
└── setup.py
```

## Requirements

- Python 3.8+
- pip
- Playwright and its browser dependencies

## Installation

```bash
git clone https://github.com/abanerjee84/google-image-scraper-clean.git
cd google-image-scraper-clean

pip install -e .
playwright install
```

Alternatively:

```bash
pip install -r requirements.txt
playwright install
```

## Command-Line Usage

Basic search:

```bash
google-image-scraper cats dogs --count 10
```

Apply resolution and output-format filters:

```bash
google-image-scraper "red roses" \
  --count 20 \
  --min-res 800x600 \
  --max-res 1920x1080 \
  --format png
```

Extract URLs without downloading images:

```bash
google-image-scraper "python programming" --dry-run --verbose
```

The short command alias can also be used where installed:

```bash
gis cats --count 5 --headless
```

## Python API

```python
import asyncio

from google_image_scraper import GoogleImageScraper, ScrapingConfig


async def main():
    config = ScrapingConfig(
        number_of_images=10,
        headless=True,
        min_resolution=(800, 600),
        max_resolution=(1920, 1080),
        image_save_format="png",
        photos_dir="downloads",
    )

    scraper = GoogleImageScraper(config)

    image_urls, downloaded_count = await scraper.scrape("cats")
    print(f"Downloaded {downloaded_count} images")

    urls = await scraper.find_image_urls("dogs")
    print(f"Found {len(urls)} URLs")


asyncio.run(main())
```

## Configuration

`ScrapingConfig` exposes the main runtime settings:

```python
from google_image_scraper import ScrapingConfig

config = ScrapingConfig(
    number_of_images=10,
    max_missed=10,
    headless=True,
    min_resolution=(800, 600),
    max_resolution=(1920, 1080),
    keep_filenames=False,
    image_save_format="jpg",
    timeout_seconds=5.0,
    scroll_attempts=3,
    click_timeout=3000,
    photos_dir="photos",
    json_dir="google_search",
)
```

## Development

Install development dependencies:

```bash
pip install -e .
pip install -r requirements-dev.txt
```

Run tests:

```bash
python -m pytest tests/
```

Code-quality tooling used by the repository includes:

```bash
mypy src/
flake8 src/
black src/
```

## Design Notes

The codebase separates scraping, configuration, CLI behaviour and utility functions so the scraper can be used either as a standalone command or as a Python library.

The asynchronous design is intended to reduce idle time during browser and network operations while keeping filtering and download behaviour configurable.

## Responsible Use

Web-scraping behaviour can be affected by website terms, robots policies, rate limits and changes to page structure. Users are responsible for ensuring that their use of the software is permitted in their jurisdiction and by the relevant service.

## License

No license file is currently included in this repository. Unless a license is added, normal copyright restrictions apply.
