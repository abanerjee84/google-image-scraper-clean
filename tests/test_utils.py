"""
Unit tests for utility functions
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    is_valid_image_url, 
    clean_search_key, 
    decode_url, 
    filter_thumbnail_urls,
    validate_resolution
)


class TestUtils(unittest.TestCase):
    
    def test_is_valid_image_url(self):
        """Test URL validation"""
        # Valid URLs
        valid_urls = [
            "https://example.com/image.jpg",
            "http://site.com/photo.png",
            "https://cdn.example.com/pic.webp",
            "https://example.com/image.jpeg?size=large"
        ]
        
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(is_valid_image_url(url))
        
        # Invalid URLs
        invalid_urls = [
            "",
            None,
            "not_a_url",
            "https://example.com/page.html",
            "ftp://example.com/image.jpg",  # Wrong protocol
            "https:///image.jpg"  # Missing domain
        ]
        
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(is_valid_image_url(url))
    
    def test_clean_search_key(self):
        """Test search key cleaning"""
        test_cases = [
            ("hello world", "hello_world"),
            ("cat/dog", "cat_dog"),
            ("my:file", "my_file"),
            ("  multiple   spaces  ", "multiple_spaces"),
            ("special<>chars", "special__chars"),
            ("normal_key", "normal_key")
        ]
        
        for input_key, expected in test_cases:
            with self.subTest(input_key=input_key):
                result = clean_search_key(input_key)
                self.assertEqual(result, expected)
    
    def test_decode_url(self):
        """Test URL decoding"""
        test_cases = [
            ("https://example.com/image%20name.jpg", "https://example.com/image name.jpg"),
            ("https://example.com/normal.jpg", "https://example.com/normal.jpg"),
            ("https://example.com/caf%C3%A9.jpg", "https://example.com/café.jpg")
        ]
        
        for encoded, expected in test_cases:
            with self.subTest(encoded=encoded):
                result = decode_url(encoded)
                self.assertEqual(result, expected)
    
    def test_filter_thumbnail_urls(self):
        """Test thumbnail URL filtering"""
        urls = [
            "https://example.com/full-resolution.jpg",
            "https://example.com/encrypted-tbn-thumbnail.jpg",
            "https://example.com/logo.png",
            "https://example.com/image/s90/small.jpg",
            "https://example.com/high-quality-image-with-long-url.jpg"
        ]
        
        thumbnail_patterns = ['encrypted-tbn', 'logo', '/s90/', '=s64']
        
        filtered = filter_thumbnail_urls(urls, thumbnail_patterns)
        
        # Should keep only full-resolution and high-quality URLs
        expected = [
            "https://example.com/full-resolution.jpg",
            "https://example.com/high-quality-image-with-long-url.jpg"
        ]
        
        self.assertEqual(filtered, expected)
    
    def test_validate_resolution(self):
        """Test resolution validation"""
        # Valid resolutions
        self.assertTrue(validate_resolution(1920, 1080, (800, 600), (2560, 1440)))
        self.assertTrue(validate_resolution(800, 600, (800, 600), (2560, 1440)))
        self.assertTrue(validate_resolution(2560, 1440, (800, 600), (2560, 1440)))
        
        # Invalid resolutions
        self.assertFalse(validate_resolution(640, 480, (800, 600), (2560, 1440)))  # Too small
        self.assertFalse(validate_resolution(3840, 2160, (800, 600), (2560, 1440)))  # Too large


if __name__ == '__main__':
    unittest.main()
