"""
Input validation and sanitization utilities
"""
import re
import os
from typing import Union, Tuple, List
from pathlib import Path
from urllib.parse import urlparse

from exceptions import ConfigurationError


def validate_search_term(search_term: str) -> str:
    """
    Validate and sanitize search term
    
    Args:
        search_term: The search term to validate
        
    Returns:
        Cleaned search term
        
    Raises:
        ConfigurationError: If search term is invalid
    """
    if not search_term or not isinstance(search_term, str):
        raise ConfigurationError("Search term must be a non-empty string")
    
    # Remove excessive whitespace
    cleaned = re.sub(r'\s+', ' ', search_term.strip())
    
    # Check length
    if len(cleaned) == 0:
        raise ConfigurationError("Search term cannot be empty")
    if len(cleaned) > 200:
        raise ConfigurationError("Search term too long (max 200 characters)")
    
    # Check for potentially problematic characters
    dangerous_chars = ['<', '>', '"', '|', '\0', '\n', '\r', '\t']
    if any(char in cleaned for char in dangerous_chars):
        raise ConfigurationError(f"Search term contains invalid characters: {dangerous_chars}")
    
    return cleaned


def validate_number_range(value: int, min_val: int, max_val: int, param_name: str) -> int:
    """
    Validate that a number is within a specified range
    
    Args:
        value: The value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        param_name: Name of the parameter for error messages
        
    Returns:
        The validated value
        
    Raises:
        ConfigurationError: If value is out of range
    """
    if not isinstance(value, int):
        raise ConfigurationError(f"{param_name} must be an integer")
    
    if value < min_val or value > max_val:
        raise ConfigurationError(
            f"{param_name} must be between {min_val} and {max_val}, got {value}"
        )
    
    return value


def validate_resolution(resolution: Union[Tuple[int, int], str]) -> Tuple[int, int]:
    """
    Validate resolution tuple or string
    
    Args:
        resolution: Resolution as (width, height) tuple or "WIDTHxHEIGHT" string
        
    Returns:
        Validated (width, height) tuple
        
    Raises:
        ConfigurationError: If resolution is invalid
    """
    if isinstance(resolution, str):
        try:
            width, height = resolution.split('x')
            resolution = (int(width), int(height))
        except (ValueError, AttributeError):
            raise ConfigurationError(f"Invalid resolution format: {resolution}. Use 'WIDTHxHEIGHT'")
    
    if not isinstance(resolution, (tuple, list)) or len(resolution) != 2:
        raise ConfigurationError("Resolution must be a tuple of (width, height)")
    
    width, height = resolution
    if not isinstance(width, int) or not isinstance(height, int):
        raise ConfigurationError("Resolution values must be integers")
    
    if width < 0 or height < 0:
        raise ConfigurationError("Resolution values must be non-negative")
    
    if width > 10000 or height > 10000:
        raise ConfigurationError("Resolution values are unreasonably large")
    
    return (width, height)


def validate_file_path(path: Union[str, Path], must_exist: bool = False, 
                      create_parent: bool = False) -> Path:
    """
    Validate file path
    
    Args:
        path: The file path to validate
        must_exist: Whether the path must already exist
        create_parent: Whether to create parent directories
        
    Returns:
        Validated Path object
        
    Raises:
        ConfigurationError: If path is invalid
    """
    if not path:
        raise ConfigurationError("Path cannot be empty")
    
    try:
        path_obj = Path(path).resolve()
    except (OSError, ValueError) as e:
        raise ConfigurationError(f"Invalid path: {e}")
    
    # Check if path exists when required
    if must_exist and not path_obj.exists():
        raise ConfigurationError(f"Path does not exist: {path_obj}")
    
    # Create parent directories if requested
    if create_parent and not path_obj.parent.exists():
        try:
            path_obj.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ConfigurationError(f"Cannot create parent directories: {e}")
    
    # Check write permissions for the parent directory
    if not must_exist:
        parent = path_obj.parent
        if parent.exists() and not os.access(parent, os.W_OK):
            raise ConfigurationError(f"No write permission for directory: {parent}")
    
    return path_obj


def validate_image_format(format_str: str) -> str:
    """
    Validate image format string
    
    Args:
        format_str: Image format (e.g., 'jpg', 'png')
        
    Returns:
        Validated format string in lowercase
        
    Raises:
        ConfigurationError: If format is not supported
    """
    if not format_str or not isinstance(format_str, str):
        raise ConfigurationError("Image format must be a non-empty string")
    
    format_str = format_str.lower().strip()
    supported_formats = {'jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp'}
    
    if format_str not in supported_formats:
        raise ConfigurationError(
            f"Unsupported image format: {format_str}. "
            f"Supported formats: {', '.join(sorted(supported_formats))}"
        )
    
    return format_str


def validate_url_list(urls: List[str], max_count: int = 1000) -> List[str]:
    """
    Validate a list of URLs
    
    Args:
        urls: List of URLs to validate
        max_count: Maximum number of URLs allowed
        
    Returns:
        List of validated URLs
        
    Raises:
        ConfigurationError: If URLs are invalid
    """
    if not isinstance(urls, list):
        raise ConfigurationError("URLs must be provided as a list")
    
    if len(urls) > max_count:
        raise ConfigurationError(f"Too many URLs: {len(urls)} (max: {max_count})")
    
    validated_urls = []
    for i, url in enumerate(urls):
        if not isinstance(url, str):
            raise ConfigurationError(f"URL at index {i} must be a string")
        
        url = url.strip()
        if not url:
            continue  # Skip empty URLs
        
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ConfigurationError(f"Invalid URL at index {i}: {url}")
            
            if parsed.scheme not in ('http', 'https'):
                raise ConfigurationError(f"URL at index {i} must use http or https: {url}")
                
        except Exception as e:
            raise ConfigurationError(f"Invalid URL at index {i}: {e}")
        
        validated_urls.append(url)
    
    return validated_urls


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    Sanitize filename for safe file system usage
    
    Args:
        filename: Original filename
        max_length: Maximum allowed length
        
    Returns:
        Sanitized filename
    """
    if not filename:
        return "unnamed"
    
    # Remove or replace problematic characters
    sanitized = re.sub(r'[<>:"/\\|?*\0]', '_', filename)
    
    # Remove control characters
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', sanitized)
    
    # Collapse multiple underscores and spaces
    sanitized = re.sub(r'[_\s]+', '_', sanitized)
    
    # Remove leading/trailing underscores and dots
    sanitized = sanitized.strip('_. ')
    
    # Ensure reasonable length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip('_. ')
    
    # Ensure we have something
    if not sanitized:
        sanitized = "unnamed"
    
    return sanitized


class ConfigValidator:
    """Validator for scraping configuration"""
    
    @staticmethod
    def validate_scraping_config(config_dict: dict) -> dict:
        """
        Validate a complete scraping configuration
        
        Args:
            config_dict: Configuration dictionary
            
        Returns:
            Validated configuration dictionary
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        validated = {}
        
        # Validate number of images
        if 'number_of_images' in config_dict:
            validated['number_of_images'] = validate_number_range(
                config_dict['number_of_images'], 1, 1000, 'number_of_images'
            )
        
        # Validate max missed
        if 'max_missed' in config_dict:
            validated['max_missed'] = validate_number_range(
                config_dict['max_missed'], 1, 100, 'max_missed'
            )
        
        # Validate resolutions
        if 'min_resolution' in config_dict:
            validated['min_resolution'] = validate_resolution(config_dict['min_resolution'])
        
        if 'max_resolution' in config_dict:
            validated['max_resolution'] = validate_resolution(config_dict['max_resolution'])
        
        # Validate paths
        if 'photos_dir' in config_dict:
            validated['photos_dir'] = validate_file_path(
                config_dict['photos_dir'], create_parent=True
            )
        
        if 'json_dir' in config_dict:
            validated['json_dir'] = validate_file_path(
                config_dict['json_dir'], create_parent=True
            )
        
        # Validate image format
        if 'image_save_format' in config_dict:
            validated['image_save_format'] = validate_image_format(
                config_dict['image_save_format']
            )
        
        # Validate timeout
        if 'timeout_seconds' in config_dict:
            timeout = config_dict['timeout_seconds']
            if not isinstance(timeout, (int, float)) or timeout <= 0:
                raise ConfigurationError("Timeout must be a positive number")
            validated['timeout_seconds'] = float(timeout)
        
        # Copy boolean values as-is (with validation)
        bool_fields = ['headless', 'keep_filenames']
        for field in bool_fields:
            if field in config_dict:
                if not isinstance(config_dict[field], bool):
                    raise ConfigurationError(f"{field} must be a boolean")
                validated[field] = config_dict[field]
        
        return validated
