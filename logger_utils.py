"""
Logging utilities for Google Image Scraper
"""
import logging
import sys
from datetime import datetime
import os

def setup_logger(name: str = "GoogleImageScraper", level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with both file and console handlers
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Create logs directory if it doesn't exist
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # File handler
    log_filename = f"{logs_dir}/scraper_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_scraping_summary(logger: logging.Logger, search_key: str, 
                        found_urls: int, downloaded_images: int, failed_downloads: int):
    """Log a summary of the scraping results"""
    logger.info(f"Scraping Summary for '{search_key}':")
    logger.info(f"  - URLs found: {found_urls}")
    logger.info(f"  - Images downloaded: {downloaded_images}")
    logger.info(f"  - Failed downloads: {failed_downloads}")
    logger.info(f"  - Success rate: {(downloaded_images/found_urls*100):.1f}%" if found_urls > 0 else "  - Success rate: 0%")
