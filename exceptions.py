"""
Custom exceptions for Google Image Scraper
"""

class GoogleImageScraperError(Exception):
    """Base exception for Google Image Scraper"""
    pass

class BrowserError(GoogleImageScraperError):
    """Raised when browser operations fail"""
    pass

class ImageDownloadError(GoogleImageScraperError):
    """Raised when image download fails"""
    def __init__(self, url: str, reason: str):
        self.url = url
        self.reason = reason
        super().__init__(f"Failed to download image from {url}: {reason}")

class InvalidResolutionError(GoogleImageScraperError):
    """Raised when image resolution doesn't meet criteria"""
    def __init__(self, actual_resolution: tuple, min_resolution: tuple, max_resolution: tuple):
        self.actual_resolution = actual_resolution
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        super().__init__(
            f"Image resolution {actual_resolution} not within bounds "
            f"[{min_resolution}, {max_resolution}]"
        )

class URLExtractionError(GoogleImageScraperError):
    """Raised when URL extraction fails"""
    pass

class FileOperationError(GoogleImageScraperError):
    """Raised when file operations fail"""
    def __init__(self, operation: str, path: str, reason: str):
        self.operation = operation
        self.path = path
        self.reason = reason
        super().__init__(f"Failed to {operation} file {path}: {reason}")

class ConfigurationError(GoogleImageScraperError):
    """Raised when configuration is invalid"""
    pass
