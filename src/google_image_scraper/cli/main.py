#!/usr/bin/env python3
"""
Command-line interface for Google Image Scraper
"""
import argparse
import asyncio
import sys
import logging
from typing import List
from pathlib import Path

from ..core.scraper import GoogleImageScraper
from ..core.config import ScrapingConfig
from ..utils.logging import setup_logger
from ..utils.helpers import clean_search_key


def parse_resolution(resolution_str: str) -> tuple:
    """Parse resolution string like '1920x1080' into tuple (1920, 1080)"""
    try:
        width, height = resolution_str.split('x')
        return (int(width), int(height))
    except (ValueError, AttributeError):
        raise argparse.ArgumentTypeError(f"Invalid resolution format: {resolution_str}. Use format: WIDTHxHEIGHT")


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        description="Scrape and download full-resolution images from Google Images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s cats dogs --count 20 --headless
  %(prog)s "red roses" --min-res 800x600 --max-res 1920x1080
  %(prog)s python logo --output ./downloads --format png
        """
    )
    
    # Positional arguments
    parser.add_argument(
        'search_terms',
        nargs='+',
        help='Search terms to scrape images for'
    )
    
    # Optional arguments
    parser.add_argument(
        '-c', '--count',
        type=int,
        default=10,
        help='Number of images to download per search term (default: 10)'
    )
    
    parser.add_argument(
        '--max-missed',
        type=int,
        default=10,
        help='Maximum number of failed downloads before stopping (default: 10)'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (no GUI)'
    )
    
    parser.add_argument(
        '--show-browser',
        action='store_true',
        help='Show browser GUI (opposite of --headless)'
    )
    
    parser.add_argument(
        '--min-res',
        type=parse_resolution,
        default='0x0',
        help='Minimum image resolution (e.g., 800x600)'
    )
    
    parser.add_argument(
        '--max-res',
        type=parse_resolution,
        default='9999x9999',
        help='Maximum image resolution (e.g., 1920x1080)'
    )
    
    parser.add_argument(
        '--format',
        choices=['jpg', 'png', 'jpeg'],
        default='jpg',
        help='Image save format (default: jpg)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default='photos',
        help='Output directory for downloaded images (default: photos)'
    )
    
    parser.add_argument(
        '--keep-filenames',
        action='store_true',
        help='Keep original filenames from URLs'
    )
    
    parser.add_argument(
        '--timeout',
        type=float,
        default=5.0,
        help='Download timeout in seconds (default: 5.0)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Extract URLs but do not download images'
    )
    
    return parser


async def scrape_single_term(
    search_term: str,
    scraper: GoogleImageScraper,
    logger,
    dry_run: bool = False
) -> dict:
    """
    Scrape images for a single search term
    
    Args:
        search_term: The search term to scrape
        scraper: GoogleImageScraper instance
        logger: Logger instance
        dry_run: If True, only extract URLs without downloading
        
    Returns:
        Dictionary with scraping results
    """
    logger.info(f"Starting scrape for: {search_term}")
    
    try:
        if dry_run:
            # Only extract URLs
            image_urls = await scraper.find_image_urls(search_term)
            logger.info(f"Dry run: Found {len(image_urls)} URLs for '{search_term}'")
            return {
                'search_term': search_term,
                'urls_found': len(image_urls),
                'images_downloaded': 0,
                'failed_downloads': 0,
                'success': True
            }
        else:
            # Full scraping workflow
            image_urls, downloaded_count = await scraper.scrape(search_term)
            failed_count = len(image_urls) - downloaded_count
            
            return {
                'search_term': search_term,
                'urls_found': len(image_urls),
                'images_downloaded': downloaded_count,
                'failed_downloads': failed_count,
                'success': True
            }
            
    except Exception as e:
        logger.error(f"Failed to scrape {search_term}: {e}")
        return {
            'search_term': search_term,
            'urls_found': 0,
            'images_downloaded': 0,
            'failed_downloads': 0,
            'success': False,
            'error': str(e)
        }


async def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(level=log_level)
    
    # Create configuration
    config = ScrapingConfig(
        number_of_images=args.count,
        max_missed=args.max_missed,
        headless=not args.show_browser if args.show_browser else True,
        min_resolution=args.min_res,
        max_resolution=args.max_res,
        keep_filenames=args.keep_filenames,
        image_save_format=args.format,
        timeout_seconds=args.timeout,
        photos_dir=str(args.output)
    )
    
    # Create scraper instance
    scraper = GoogleImageScraper(config)
    
    logger.info("Starting Google Image Scraper")
    logger.info(f"Search terms: {args.search_terms}")
    logger.info(f"Images per term: {config.number_of_images}")
    logger.info(f"Output directory: {config.photos_dir}")
    
    if args.dry_run:
        logger.info("DRY RUN MODE: URLs will be extracted but images will not be downloaded")
    
    # Process search terms
    results = []
    for search_term in args.search_terms:
        result = await scrape_single_term(search_term, scraper, logger, args.dry_run)
        results.append(result)
    
    # Print summary
    print("\n" + "="*60)
    print("SCRAPING SUMMARY")
    print("="*60)
    
    total_urls = sum(r['urls_found'] for r in results)
    total_downloaded = sum(r['images_downloaded'] for r in results)
    total_failed = sum(r['failed_downloads'] for r in results)
    successful_terms = sum(1 for r in results if r['success'])
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['search_term']}: {result['urls_found']} URLs, "
              f"{result['images_downloaded']} downloaded")
        if not result['success']:
            print(f"   Error: {result.get('error', 'Unknown error')}")
    
    print(f"\nOverall: {successful_terms}/{len(args.search_terms)} terms successful")
    print(f"Total URLs found: {total_urls}")
    print(f"Total images downloaded: {total_downloaded}")
    print(f"Total failed downloads: {total_failed}")
    
    if total_urls > 0:
        success_rate = (total_downloaded / total_urls) * 100
        print(f"Success rate: {success_rate:.1f}%")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Script failed: {e}")
        sys.exit(1)
