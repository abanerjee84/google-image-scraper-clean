#!/usr/bin/env python3
"""
Simple example showing how to use the new modular Google Image Scraper
"""

import asyncio
import sys
import os

# Add the src directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from google_image_scraper import GoogleImageScraper, ScrapingConfig


async def simple_example():
    """Simple example: scrape 5 cat images"""
    print("🐱 Scraping 5 cat images...")
    
    # Create a scraper with custom configuration
    config = ScrapingConfig(
        number_of_images=5,
        headless=True,  # Set to False to see browser
        photos_dir='example_photos'
    )
    
    scraper = GoogleImageScraper(config)
    
    try:
        # Scrape images (this finds URLs and downloads them)
        image_urls, downloaded_count = await scraper.scrape('cat')
        
        print(f"✅ Found {len(image_urls)} URLs")
        print(f"📥 Downloaded {downloaded_count} images")
        print("🎉 Done! Check the 'example_photos/cat' folder")
        
    except Exception as e:
        print(f"❌ Error: {e}")


async def advanced_example():
    """Advanced example with custom settings"""
    print("🔧 Advanced scraping example...")
    
    # Create scraper with advanced configuration
    config = ScrapingConfig(
        number_of_images=10,
        headless=True,
        min_resolution=(800, 600),  # Minimum 800x600 resolution
        max_resolution=(1920, 1080),  # Maximum 1920x1080 resolution
        image_save_format='png',  # Save as PNG
        timeout_seconds=10.0,  # 10 second timeout
        photos_dir='advanced_photos'
    )
    
    scraper = GoogleImageScraper(config)
    
    search_terms = ['python programming', 'machine learning', 'data science']
    
    for search_term in search_terms:
        print(f"\n🔍 Searching for: {search_term}")
        try:
            image_urls, downloaded_count = await scraper.scrape(search_term)
            print(f"   ✅ {downloaded_count}/{len(image_urls)} images downloaded")
        except Exception as e:
            print(f"   ❌ Failed: {e}")


async def url_only_example():
    """Example: Only extract URLs without downloading"""
    print("🔗 URL extraction only example...")
    
    scraper = GoogleImageScraper()
    
    try:
        # Only find URLs, don't download
        image_urls = await scraper.find_image_urls('space exploration')
        
        print(f"✅ Found {len(image_urls)} URLs:")
        for i, url in enumerate(image_urls[:3], 1):
            print(f"   {i}. {url[:80]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    """Run all examples"""
    print("🚀 Google Image Scraper Examples\n")
    
    print("=" * 50)
    await simple_example()
    
    print("\n" + "=" * 50)
    await advanced_example()
    
    print("\n" + "=" * 50)
    await url_only_example()
    
    print("\n🎉 All examples completed!")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Examples interrupted by user")
    except Exception as e:
        print(f"[ERROR] Examples failed: {e}")
