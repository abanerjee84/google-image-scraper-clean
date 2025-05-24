"""
Configuration settings for Google Image Scraper
"""
import os
from dataclasses import dataclass
from typing import Tuple, List, Optional

@dataclass
class ScrapingConfig:
    """Configuration for scraping parameters"""
    number_of_images: int = 10
    max_missed: int = 10
    headless: bool = True
    min_resolution: Tuple[int, int] = (0, 0)
    max_resolution: Tuple[int, int] = (9999, 9999)
    keep_filenames: bool = False
    image_save_format: str = 'jpg'
    timeout_seconds: float = 5.0
    scroll_attempts: int = 3
    click_timeout: int = 3000
    
    # Directory settings
    photos_dir: str = 'photos'
    json_dir: str = 'google_search'
    
    # URL filtering patterns
    thumbnail_patterns: Optional[List[str]] = None
    logo_patterns: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.thumbnail_patterns is None:
            self.thumbnail_patterns = [
                'encrypted-tbn', 'logo', 'favicon', '/s90/', '/s100/', 
                '/s150/', '=s64', '=s90', '=s100'
            ]
        if self.logo_patterns is None:
            self.logo_patterns = ['logo', 'favicon']

# Default configuration instance
DEFAULT_CONFIG = ScrapingConfig()
