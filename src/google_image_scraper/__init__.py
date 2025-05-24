"""
Google Image Scraper - A professional Python package for scraping Google Images

This package provides a clean, modular interface for searching and downloading
images from Google Images with advanced filtering and configuration options.
"""

from .core.scraper import GoogleImageScraper
from .core.config import ScrapingConfig, DEFAULT_CONFIG
from .core.exceptions import (
    BrowserError, 
    ImageDownloadError, 
    InvalidResolutionError,
    URLExtractionError, 
    FileOperationError
)

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "GoogleImageScraper",
    "ScrapingConfig", 
    "DEFAULT_CONFIG",
    "BrowserError",
    "ImageDownloadError", 
    "InvalidResolutionError",
    "URLExtractionError",
    "FileOperationError"
]
