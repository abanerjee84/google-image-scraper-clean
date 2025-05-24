from typing import List, Tuple, Optional
import os
import io
import json
from datetime import datetime
import urllib.parse

import httpx
from PIL import Image
from playwright.async_api._generated import Locator
from playwright.async_api import async_playwright

from config import DEFAULT_CONFIG
from logger_utils import setup_logger
from utils import decode_url, filter_thumbnail_urls, validate_resolution, is_valid_image_url
from exceptions import (
    BrowserError, ImageDownloadError, InvalidResolutionError, 
    URLExtractionError, FileOperationError
)

def google_images_url(search_key: str) -> str:
    """Generate Google Images search URL for the given search key"""
    encoded_key = urllib.parse.quote(search_key)
    return f'https://www.google.com/search?q={encoded_key}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947'

def save_urls_to_json(image_urls: List[str], search_key: str, base_dir: str = 'google_search') -> Optional[str]:
    """
    Save image URLs to a JSON file in the google_search folder.
    
    Args:
        image_urls: List of image URLs
        search_key: The search term used
        base_dir: Base directory to save the JSON file
        
    Returns:
        Path to the saved JSON file, or None if saving failed
        
    Raises:
        FileOperationError: If file operations fail
    """
    logger = setup_logger()
    
    try:
        # Create google_search directory if it doesn't exist
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            logger.info(f'Created directory: {base_dir}')
        
        # Clean and decode URLs
        cleaned_urls = [decode_url(url) for url in image_urls]
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{search_key}_{timestamp}.json"
        filepath = os.path.join(base_dir, filename)
        
        # Prepare data structure
        data = {
            "search_key": search_key,
            "timestamp": datetime.now().isoformat(),
            "total_urls": len(cleaned_urls),
            "image_urls": cleaned_urls
        }
        
        # Save to JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f'Saved {len(cleaned_urls)} URLs to: {filepath}')
        return filepath
        
    except OSError as e:
        raise FileOperationError("save", filepath, str(e))
    except Exception as e:
        logger.error(f'Failed to save URLs to JSON: {e}')
        return None

async def find_image_urls(
    search_key='cat',
    number_of_images=1,
    max_missed=10,
    headless=False,
):
    """
        This function searches and return a list of full-resolution image urls based on the search key.
        Uses advanced extraction methods to get actual full-size images, not thumbnails.

        Example:
            image_urls = find_image_urls(search_key, number_of_images)
    """
    print(f'[INFO] Gathering full-resolution image links for {search_key}')
    
    # Open playwright browser
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=headless)
        try:
            page = await browser.new_page()
            
            # Open google images page with search query
            await page.goto(google_images_url(search_key))
            
            # Wait for page to load completely
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(3000)
            
            print(f"[INFO] Page loaded, extracting full-resolution URLs...")
            
            # Extract full-resolution URLs from the page's JavaScript data
            full_res_urls = await page.evaluate("""
                () => {
                    const fullResUrls = [];
                    
                    // Method 1: Look for URLs in script tags containing image data
                    const scripts = document.querySelectorAll('script');
                    for (const script of scripts) {
                        const content = script.textContent || script.innerHTML;
                        if (content.includes('["') && content.includes('http')) {
                            // Find URLs that look like full resolution images
                            const urlMatches = content.match(/https?:\/\/[^\s"',\]]+\.(jpg|jpeg|png|webp|gif)([?&][^\s"',\]]*)?/gi);
                            if (urlMatches) {
                                for (const url of urlMatches) {
                                    // Filter out obvious thumbnails and small images
                                    if (!url.includes('encrypted-tbn') && 
                                        !url.includes('logo') && 
                                        !url.includes('favicon') &&
                                        !url.includes('/s90/') &&
                                        !url.includes('/s100/') &&
                                        !url.includes('/s150/') &&
                                        !url.includes('=s64') &&
                                        !url.includes('=s90') &&
                                        !url.includes('=s100')) {
                                        fullResUrls.push(url);
                                    }
                                }
                            }
                        }
                    }
                    
                    // Method 2: Look for data in meta tags and other elements
                    const metaTags = document.querySelectorAll('meta');
                    for (const meta of metaTags) {
                        const content = meta.getAttribute('content') || '';
                        if (content.includes('http') && (content.includes('.jpg') || content.includes('.png'))) {
                            const urlMatch = content.match(/https?:\/\/[^\s"']+\.(jpg|jpeg|png|webp|gif)/i);
                            if (urlMatch && !urlMatch[0].includes('encrypted-tbn')) {
                                fullResUrls.push(urlMatch[0]);
                            }
                        }
                    }
                    
                    // Method 3: Look in all text content for image URLs
                    const allText = document.documentElement.innerHTML;
                    const allUrlMatches = allText.match(/https?:\/\/[^\s"',\](){}]+\.(jpg|jpeg|png|webp|gif)([?&][^\s"',\](){}]*)?/gi);
                    if (allUrlMatches) {
                        for (const url of allUrlMatches) {
                            if (!url.includes('encrypted-tbn') && 
                                !url.includes('logo') && 
                                !url.includes('favicon') &&
                                url.length > 50) { // Longer URLs tend to be full resolution
                                fullResUrls.push(url);
                            }
                        }
                    }
                    
                    // Remove duplicates and filter
                    const uniqueUrls = [...new Set(fullResUrls)];
                    
                    // Sort by URL length (longer URLs often indicate higher resolution)
                    return uniqueUrls.sort((a, b) => b.length - a.length);
                }
            """)
            
            print(f"[INFO] Found {len(full_res_urls)} potential full-resolution URLs from page data")
            
            # If we didn't find enough full-res URLs, try clicking on images to get them
            if len(full_res_urls) < number_of_images:
                print(f"[INFO] Trying to extract more URLs by clicking on images...")
                
                # Scroll and load more images first
                scroll_attempts = max(3, (number_of_images // 10) + 1)
                for i in range(scroll_attempts):
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await page.wait_for_timeout(2000)
                
                # Find clickable image containers
                image_containers = await page.locator('div[data-ved]:has(img)').all()
                
                clicked_urls = []
                max_attempts = min(len(image_containers), number_of_images * 2)  # Try more than needed
                
                for i, container in enumerate(image_containers[:max_attempts]):
                    if len(clicked_urls) >= number_of_images:
                        break
                        
                    try:
                        # Click on the container
                        await container.click(timeout=3000)
                        await page.wait_for_timeout(1000)
                        
                        # Try to find the full resolution image
                        full_img_selectors = [
                            'img[src*="http"]:not([src*="encrypted-tbn"])',
                            'img[data-src*="http"]:not([data-src*="encrypted-tbn"])',
                            '.n3VNCb',
                            '.iPVvYb'
                        ]
                        
                        for selector in full_img_selectors:
                            try:
                                img_element = page.locator(selector).first
                                await img_element.wait_for(timeout=2000, state='visible')
                                img_src = await img_element.get_attribute('src') or await img_element.get_attribute('data-src')
                                if img_src and 'http' in img_src and not 'encrypted-tbn' in img_src and len(img_src) > 50:
                                    clicked_urls.append(img_src)
                                    print(f"[DEBUG] Extracted URL {len(clicked_urls)}: {img_src[:80]}...")
                                    break
                            except:
                                continue
                        
                        # Close the image by clicking elsewhere or pressing escape
                        await page.keyboard.press('Escape')
                        await page.wait_for_timeout(500)
                        
                    except Exception as e:
                        # Don't print every error, just continue
                        continue
                
                # Combine both methods
                full_res_urls.extend(clicked_urls)
                full_res_urls = list(dict.fromkeys(full_res_urls))  # Remove duplicates while preserving order
                print(f"[INFO] Added {len(clicked_urls)} URLs from clicking images")
            
            # Limit to requested number
            image_urls = full_res_urls[:number_of_images]
            
            # Clean and decode URLs before returning
            cleaned_image_urls = []
            for url in image_urls:
                try:
                    # First decode unicode escapes like \u003d
                    cleaned_url = url.encode('utf-8').decode('unicode_escape')
                    # Then decode URL encoding like %20
                    cleaned_url = urllib.parse.unquote(cleaned_url)
                    cleaned_image_urls.append(cleaned_url)
                except Exception:
                    # If decoding fails, use original URL
                    cleaned_image_urls.append(url)
            
            await page.close()
        finally:
            # Ensure browser is properly closed even if an exception occurs
            await browser.close()
        
        # Save URLs to JSON file
        if cleaned_image_urls:
            save_urls_to_json(cleaned_image_urls, search_key)
        
        print(f'[INFO] Google search ended for {search_key}. Found {len(cleaned_image_urls)} full-resolution image urls.')
        
        # Show sample URLs for verification
        for i, url in enumerate(cleaned_image_urls[:3]):
            print(f'[SAMPLE] {i+1}. {url[:100]}...')
        
        return cleaned_image_urls

async def save_images(
        image_urls: List[str],
        image_save_format='jpg',
        images_dir_path='photos',
        keep_filenames = False,
        image_file_prefix = 'image',
        min_resolution=(0, 0),
        max_resolution=(1920, 1080),
    ):
    #save images into file directory
    """
        This function takes in an array of image urls and saves it into the given image path/directory.
        Example:
            image_urls=['https://example_1.jpg','https://example_2.jpg']
            save_images(image_urls)

    """
    if not os.path.exists(images_dir_path):
        print(f'[INFO] Image dir path {images_dir_path} not found. Creating a new folder.')
        os.makedirs(images_dir_path)

    print(f'[INFO] Saving {image_file_prefix} images, please wait...')
    for index, image_url in enumerate(image_urls):
        image_resp = await download_image(image_url)
        if not image_resp:
            continue
        try:
            with Image.open(io.BytesIO(image_resp.content)) as image_from_web:
                is_image_resolution_valid = check_if_image_resolution_valid(image_from_web, min_resolution, max_resolution)
                if not is_image_resolution_valid:
                    print(f'[INFO] Skipping image as resolution is {image_from_web.size}')
                    continue
                image_name = f'{image_file_prefix}-{index}'
                image_path = save_image(image_from_web, images_dir_path, image_name, save_format=image_save_format)
                print(f'[INFO] {image_file_prefix} \t {index} \t Image saved at: {image_path}')
                image_from_web.close()
        except Exception as e:
            print(f'[ERROR] Failed to save downloaded image with url {image_url}. Error: ', e)
    print('--------------------------------------------------')
    print(f'[INFO] Downloading and saving {image_file_prefix} images completed. Please note that some photos may not have been downloaded as they were not in the correct format (e.g. jpg, jpeg, png)')


async def download_image(image_url: str):
    try:
        timeout = httpx.Timeout(5.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            image_resp = await client.get(image_url)
            if image_resp.status_code == 200:
                return image_resp
            else:
                image_resp.raise_for_status()
    except httpx.TimeoutException:
        print(f'[ERROR] Image download timeout for url {image_url}')
    except Exception as e:
        print(f'[ERROR] Image download failed for url {image_url}. Error: ', e)
    return None


def check_if_image_resolution_valid(image: Image.Image, min_resolution: Tuple[int, int], max_resolution: Tuple[int, int]):
    image_resolution = image.size
    if image_resolution:
        if (
            image_resolution[0] >= min_resolution[0]and
            image_resolution[0] <= max_resolution[0] and
            image_resolution[1] >= min_resolution[1] and
            image_resolution[1] <= max_resolution[1]
        ):
            return True
    return False


def save_image(image: Image.Image, images_dir_path: str, image_name: str, save_format: str = None):
    image_original_format = image.format.lower()
    if not save_format or (save_format not in ['jpg', 'png', 'jpeg']):
        save_format = image_original_format
    image_filename = f'{image_name}.{save_format}'
    image_path = os.path.join(images_dir_path, image_filename)
    try:
        if image_original_format != save_format:
            image = image.convert('RGB')
    except Exception as e:
        image = image.convert('RGB')
    image.save(image_path)
    return image_path
