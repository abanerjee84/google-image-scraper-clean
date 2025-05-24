#!/usr/bin/env python3
"""
Simple example script showing how to use the Google Image Scraper
"""

import asyncio
from GoogleImageScraper import find_image_urls, save_images

async def simple_example():
    """Simple example: scrape 5 cat images"""
    print("🐱 Scraping 5 cat images...")
    
    # Extract image URLs
    image_urls = await find_image_urls(
        search_key='cat',
        number_of_images=5,
        headless=True  # Set to False to see browser
    )
    
    if image_urls:
        print(f"✅ Found {len(image_urls)} URLs")
        
        # Download the images
        await save_images(
            image_urls=image_urls,
            images_dir_path='example_photos',
            image_file_prefix='cat'
        )
        
        print("🎉 Done! Check the 'example_photos' folder")
    else:
        print("❌ No URLs found")

if __name__ == '__main__':
    asyncio.run(simple_example())
