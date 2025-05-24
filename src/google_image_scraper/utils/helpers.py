"""
Utility functions for Google Image Scraper
"""
from typing import List, Optional, Tuple, Dict, Any
import re
import urllib.parse
from urllib.parse import urlparse
import mimetypes

def is_valid_image_url(url: str) -> bool:
    """
    Check if a URL points to a valid image
    
    Args:
        url: The URL to validate
        
    Returns:
        True if the URL appears to be a valid image URL
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
        
        # Check file extension
        path = parsed.path.lower()
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}
        if any(path.endswith(ext) for ext in image_extensions):
            return True
        
        # Check MIME type if possible
        mime_type, _ = mimetypes.guess_type(url)
        if mime_type and mime_type.startswith('image/'):
            return True
            
        return False
    except Exception:
        return False

def clean_search_key(search_key: str) -> str:
    """
    Clean and normalize search key for use in filenames
    
    Args:
        search_key: The original search term
        
    Returns:
        Cleaned search key safe for use in filenames
    """
    # Remove or replace invalid filename characters
    cleaned = re.sub(r'[<>:"/\\|?*]', '_', search_key)
    # Remove multiple spaces and trim
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    # Replace spaces with underscores
    cleaned = cleaned.replace(' ', '_')
    return cleaned

def decode_url(url: str) -> str:
    """
    Decode URL-encoded characters and unicode escapes
    
    Args:
        url: The URL to decode
        
    Returns:
        Decoded URL
    """
    try:
        # First decode unicode escapes like \u003d
        decoded = url.encode('utf-8').decode('unicode_escape')
        # Then decode URL encoding like %20
        decoded = urllib.parse.unquote(decoded)
        return decoded
    except Exception:
        return url

def filter_thumbnail_urls(urls: List[str], thumbnail_patterns: List[str]) -> List[str]:
    """
    Filter out thumbnail and low-quality image URLs
    
    Args:
        urls: List of URLs to filter
        thumbnail_patterns: Patterns that indicate thumbnail URLs
        
    Returns:
        Filtered list of URLs
    """
    filtered_urls = []
    for url in urls:
        is_thumbnail = any(pattern in url.lower() for pattern in thumbnail_patterns)
        if not is_thumbnail and len(url) > 50:  # Longer URLs often indicate full resolution
            filtered_urls.append(url)
    return filtered_urls

def validate_resolution(width: int, height: int, 
                       min_resolution: Tuple[int, int], 
                       max_resolution: Tuple[int, int]) -> bool:
    """
    Check if image resolution is within specified bounds
    
    Args:
        width: Image width
        height: Image height
        min_resolution: Minimum (width, height)
        max_resolution: Maximum (width, height)
        
    Returns:
        True if resolution is valid
    """
    return (min_resolution[0] <= width <= max_resolution[0] and
            min_resolution[1] <= height <= max_resolution[1])

def create_progress_callback(total: int, search_key: str):
    """
    Create a progress callback function for tracking download progress
    
    Args:
        total: Total number of items to process
        search_key: The search term being processed
        
    Returns:
        Progress callback function
    """
    def progress(current: int, item_name: str = "item"):
        percentage = (current / total) * 100 if total > 0 else 0
        print(f"[{search_key}] Progress: {current}/{total} ({percentage:.1f}%) - {item_name}")
    
    return progress
