"""
Main Google Image Scraper class
"""
from typing import List, Tuple, Optional
import os
import io
import json
from datetime import datetime
import urllib.parse

import httpx
from PIL import Image
from playwright.async_api import async_playwright

from .config import ScrapingConfig, DEFAULT_CONFIG
from .exceptions import (
    BrowserError, ImageDownloadError, InvalidResolutionError, 
    URLExtractionError, FileOperationError
)
from ..utils.helpers import decode_url, filter_thumbnail_urls, validate_resolution, is_valid_image_url
from ..utils.logging import setup_logger, log_scraping_summary


class GoogleImageScraper:
    """
    A professional Google Image Scraper with advanced features
    """
    
    def __init__(self, config: Optional[ScrapingConfig] = None):
        """
        Initialize the scraper with configuration
        
        Args:
            config: Scraping configuration, uses DEFAULT_CONFIG if None
        """
        self.config = config or DEFAULT_CONFIG
        self.logger = setup_logger()
        
    def _generate_search_url(self, search_key: str) -> str:
        """Generate Google Images search URL for the given search key"""
        encoded_key = urllib.parse.quote(search_key)
        return f'https://www.google.com/search?q={encoded_key}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947'

    def _save_urls_to_json(self, image_urls: List[str], search_key: str) -> Optional[str]:
        """
        Save image URLs to a JSON file in the configured directory.
        
        Args:
            image_urls: List of image URLs
            search_key: The search term used
            
        Returns:
            Path to the saved JSON file, or None if saving failed
            
        Raises:
            FileOperationError: If file operations fail
        """
        try:
            # Create directory if it doesn't exist
            if not os.path.exists(self.config.json_dir):
                os.makedirs(self.config.json_dir)
                self.logger.info(f'Created directory: {self.config.json_dir}')
            
            # Clean and decode URLs
            cleaned_urls = [decode_url(url) for url in image_urls]
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{search_key}_{timestamp}.json"
            filepath = os.path.join(self.config.json_dir, filename)
            
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
            self.logger.info(f'Saved {len(cleaned_urls)} URLs to: {filepath}')
            return filepath
            
        except OSError as e:
            raise FileOperationError("save", filepath, str(e))
        except Exception as e:
            self.logger.error(f'Failed to save URLs to JSON: {e}')
            return None

    async def find_image_urls(self, search_key: str) -> List[str]:
        """
        Search and return a list of full-resolution image URLs based on the search key.
        Uses advanced extraction methods to get actual full-size images, not thumbnails.

        Args:
            search_key: The search term to use
            
        Returns:
            List of image URLs
            
        Raises:
            BrowserError: If browser operations fail
            URLExtractionError: If URL extraction fails
        """
        self.logger.info(f'Gathering full-resolution image links for "{search_key}"')
        
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=self.config.headless)
                try:
                    page = await browser.new_page()
                    
                    # Navigate to Google Images search
                    search_url = self._generate_search_url(search_key)
                    await page.goto(search_url)
                    
                    # Wait for page to load completely
                    await page.wait_for_load_state('networkidle')
                    await page.wait_for_timeout(3000)
                    
                    self.logger.info("Page loaded, extracting full-resolution URLs...")
                    
                    # Extract full-resolution URLs from the page's JavaScript data
                    full_res_urls = await self._extract_urls_from_page_data(page)
                    
                    self.logger.info(f"Found {len(full_res_urls)} potential full-resolution URLs from page data")
                    
                    # If we didn't find enough full-res URLs, try clicking on images
                    if len(full_res_urls) < self.config.number_of_images:
                        self.logger.info("Trying to extract more URLs by clicking on images...")
                        clicked_urls = await self._extract_urls_by_clicking(page)
                        full_res_urls.extend(clicked_urls)
                        full_res_urls = list(dict.fromkeys(full_res_urls))  # Remove duplicates
                        self.logger.info(f"Added {len(clicked_urls)} URLs from clicking images")
                    
                    # Limit to requested number and clean URLs
                    image_urls = full_res_urls[:self.config.number_of_images]
                    cleaned_image_urls = [decode_url(url) for url in image_urls]
                    
                    await page.close()
                finally:
                    await browser.close()
                
                # Save URLs to JSON file
                if cleaned_image_urls:
                    self._save_urls_to_json(cleaned_image_urls, search_key)
                
                self.logger.info(f'Google search completed for "{search_key}". Found {len(cleaned_image_urls)} full-resolution image URLs.')
                
                # Show sample URLs for verification
                for i, url in enumerate(cleaned_image_urls[:3]):
                    self.logger.debug(f'Sample {i+1}: {url[:100]}...')
                
                return cleaned_image_urls
                
        except Exception as e:
            raise BrowserError(f"Failed to extract URLs: {str(e)}")

    async def _extract_urls_from_page_data(self, page) -> List[str]:
        """Extract full-resolution URLs from page's JavaScript data"""
        return await page.evaluate("""
            () => {
                const fullResUrls = [];
                
                // Method 1: Look for URLs in script tags containing image data
                const scripts = document.querySelectorAll('script');
                for (const script of scripts) {
                    const content = script.textContent || script.innerHTML;
                    if (content.includes('["') && content.includes('http')) {
                        const urlMatches = content.match(/https?:\\/\\/[^\\s"',\\]]+\\.(jpg|jpeg|png|webp|gif)([?&][^\\s"',\\]]*)?/gi);
                        if (urlMatches) {
                            for (const url of urlMatches) {
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
                
                // Method 2: Look for data in meta tags
                const metaTags = document.querySelectorAll('meta');
                for (const meta of metaTags) {
                    const content = meta.getAttribute('content') || '';
                    if (content.includes('http') && (content.includes('.jpg') || content.includes('.png'))) {
                        const urlMatch = content.match(/https?:\\/\\/[^\\s"']+\\.(jpg|jpeg|png|webp|gif)/i);
                        if (urlMatch && !urlMatch[0].includes('encrypted-tbn')) {
                            fullResUrls.push(urlMatch[0]);
                        }
                    }
                }
                
                // Method 3: Look in all text content for image URLs
                const allText = document.documentElement.innerHTML;
                const allUrlMatches = allText.match(/https?:\\/\\/[^\\s"',\\](){}]+\\.(jpg|jpeg|png|webp|gif)([?&][^\\s"',\\](){}]*)?/gi);
                if (allUrlMatches) {
                    for (const url of allUrlMatches) {
                        if (!url.includes('encrypted-tbn') && 
                            !url.includes('logo') && 
                            !url.includes('favicon') &&
                            url.length > 50) {
                            fullResUrls.push(url);
                        }
                    }
                }
                
                // Remove duplicates and sort by URL length
                const uniqueUrls = [...new Set(fullResUrls)];
                return uniqueUrls.sort((a, b) => b.length - a.length);
            }
        """)

    async def _extract_urls_by_clicking(self, page) -> List[str]:
        """Extract URLs by clicking on image containers"""
        # Scroll and load more images first
        for i in range(self.config.scroll_attempts):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
        
        # Find clickable image containers
        image_containers = await page.locator('div[data-ved]:has(img)').all()
        
        clicked_urls = []
        max_attempts = min(len(image_containers), self.config.number_of_images * 2)
        
        for i, container in enumerate(image_containers[:max_attempts]):
            if len(clicked_urls) >= self.config.number_of_images:
                break
                
            try:
                # Click on the container
                await container.click(timeout=self.config.click_timeout)
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
                        if img_src and 'http' in img_src and 'encrypted-tbn' not in img_src and len(img_src) > 50:
                            clicked_urls.append(img_src)
                            self.logger.debug(f"Extracted URL {len(clicked_urls)}: {img_src[:80]}...")
                            break
                    except:
                        continue
                
                # Close the image by pressing escape
                await page.keyboard.press('Escape')
                await page.wait_for_timeout(500)
                
            except Exception:
                continue
        
        return clicked_urls

    async def save_images(self, image_urls: List[str], search_key: str) -> int:
        """
        Save images from URLs to the configured directory
        
        Args:
            image_urls: List of image URLs to download
            search_key: Search term used (for directory naming)
            
        Returns:
            Number of successfully downloaded images
        """
        # Create directory for this search
        images_dir = os.path.join(self.config.photos_dir, search_key)
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
            self.logger.info(f'Created directory: {images_dir}')

        self.logger.info(f'Saving {len(image_urls)} images for "{search_key}"...')
        
        downloaded_count = 0
        failed_count = 0
        
        for index, image_url in enumerate(image_urls):
            try:
                image_resp = await self._download_image(image_url)
                if not image_resp:
                    failed_count += 1
                    continue
                
                with Image.open(io.BytesIO(image_resp.content)) as image_from_web:
                    # Validate resolution
                    if not self._validate_image_resolution(image_from_web):
                        self.logger.info(f'Skipping image {index} as resolution {image_from_web.size} is invalid')
                        failed_count += 1
                        continue
                    
                    # Save image
                    image_name = f'{search_key}-{index}'
                    image_path = self._save_image(image_from_web, images_dir, image_name)
                    self.logger.info(f'Image {index} saved at: {image_path}')
                    downloaded_count += 1
                    
            except Exception as e:
                self.logger.error(f'Failed to save image {index} from {image_url}: {e}')
                failed_count += 1
        
        # Log summary
        log_scraping_summary(self.logger, search_key, len(image_urls), downloaded_count, failed_count)
        return downloaded_count

    async def _download_image(self, image_url: str) -> Optional[httpx.Response]:
        """Download image from URL"""
        try:
            timeout = httpx.Timeout(self.config.timeout_seconds)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(image_url)
                if response.status_code == 200:
                    return response
                else:
                    response.raise_for_status()
        except httpx.TimeoutException:
            self.logger.error(f'Image download timeout for URL: {image_url}')
        except Exception as e:
            self.logger.error(f'Image download failed for URL {image_url}: {e}')
        return None

    def _validate_image_resolution(self, image: Image.Image) -> bool:
        """Check if image resolution meets the configured criteria"""
        return validate_resolution(
            image.size[0], image.size[1],
            self.config.min_resolution, 
            self.config.max_resolution
        )

    def _save_image(self, image: Image.Image, images_dir: str, image_name: str) -> str:
        """Save image to disk with the configured format"""
        image_format = self.config.image_save_format
        image_filename = f'{image_name}.{image_format}'
        image_path = os.path.join(images_dir, image_filename)
        
        try:
            if image.format and image.format.lower() != image_format:
                image = image.convert('RGB')
            image.save(image_path)
        except Exception:
            # Fallback to RGB conversion
            image = image.convert('RGB')
            image.save(image_path)
            
        return image_path

    async def scrape(self, search_key: str) -> Tuple[List[str], int]:
        """
        Complete scraping workflow: find URLs and download images
        
        Args:
            search_key: The search term to use
            
        Returns:
            Tuple of (image_urls, downloaded_count)
        """
        try:
            # Find image URLs
            image_urls = await self.find_image_urls(search_key)
            
            # Download images
            downloaded_count = await self.save_images(image_urls, search_key)
            
            return image_urls, downloaded_count
            
        except Exception as e:
            self.logger.error(f'Scraping failed for "{search_key}": {e}')
            raise
