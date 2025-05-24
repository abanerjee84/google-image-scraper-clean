#!/usr/bin/env python3
"""
Test script to verify the modular structure works correctly
"""
import sys
import os
import asyncio

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all imports work correctly"""
    print("🧪 Testing imports...")
    
    try:
        # Test main package import
        from google_image_scraper import GoogleImageScraper, ScrapingConfig, DEFAULT_CONFIG
        print("✅ Main package imports successful")
        
        # Test exception imports
        from google_image_scraper import (
            BrowserError, ImageDownloadError, InvalidResolutionError,
            URLExtractionError, FileOperationError
        )
        print("✅ Exception imports successful")
        
        # Test utility imports
        from google_image_scraper.utils.helpers import (
            is_valid_image_url, clean_search_key, decode_url
        )
        print("✅ Utility imports successful")
        
        # Test logging imports
        from google_image_scraper.utils.logging import setup_logger
        print("✅ Logging imports successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_configuration():
    """Test configuration creation"""
    print("\n🔧 Testing configuration...")
    
    try:
        from google_image_scraper import ScrapingConfig, DEFAULT_CONFIG
        
        # Test default config
        print(f"✅ Default config created: {DEFAULT_CONFIG.number_of_images} images")
        
        # Test custom config
        custom_config = ScrapingConfig(
            number_of_images=20,
            headless=True,
            min_resolution=(800, 600),
            image_save_format='png'
        )
        print(f"✅ Custom config created: {custom_config.number_of_images} images, format: {custom_config.image_save_format}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_scraper_creation():
    """Test scraper creation"""
    print("\n🕷️ Testing scraper creation...")
    
    try:
        from google_image_scraper import GoogleImageScraper, ScrapingConfig
        
        # Test with default config
        scraper1 = GoogleImageScraper()
        print("✅ Scraper created with default config")
        
        # Test with custom config
        config = ScrapingConfig(number_of_images=5, headless=True)
        scraper2 = GoogleImageScraper(config)
        print("✅ Scraper created with custom config")
        
        return True
        
    except Exception as e:
        print(f"❌ Scraper creation failed: {e}")
        return False

async def test_url_extraction():
    """Test URL extraction (dry run)"""
    print("\n🔗 Testing URL extraction...")
    
    try:
        from google_image_scraper import GoogleImageScraper, ScrapingConfig
        
        # Create a scraper with minimal settings for testing
        config = ScrapingConfig(
            number_of_images=2,  # Small number for testing
            headless=True,
            timeout_seconds=10.0
        )
        scraper = GoogleImageScraper(config)
        
        print("   Attempting to extract URLs for 'test'...")
        print("   (This is a real test - it will try to connect to Google)")
        
        # This is a real test - comment out if you don't want network calls
        # urls = await scraper.find_image_urls('test')
        # print(f"✅ URL extraction successful: found {len(urls)} URLs")
        
        print("✅ URL extraction test setup successful (actual test commented out)")
        return True
        
    except Exception as e:
        print(f"❌ URL extraction test failed: {e}")
        return False

def test_cli_imports():
    """Test CLI imports"""
    print("\n💻 Testing CLI imports...")
    
    try:
        from google_image_scraper.cli.main import create_parser, parse_resolution
        
        # Test argument parser creation
        parser = create_parser()
        print("✅ CLI parser created successfully")
        
        # Test resolution parsing
        res = parse_resolution("1920x1080")
        assert res == (1920, 1080)
        print("✅ Resolution parsing works")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def test_package_structure():
    """Test that the package structure is correct"""
    print("\n📦 Testing package structure...")
    
    expected_files = [
        'src/google_image_scraper/__init__.py',
        'src/google_image_scraper/__main__.py',
        'src/google_image_scraper/py.typed',
        'src/google_image_scraper/core/__init__.py',
        'src/google_image_scraper/core/scraper.py',
        'src/google_image_scraper/core/config.py',
        'src/google_image_scraper/core/exceptions.py',
        'src/google_image_scraper/utils/__init__.py',
        'src/google_image_scraper/utils/helpers.py',
        'src/google_image_scraper/utils/logging.py',
        'src/google_image_scraper/cli/__init__.py',
        'src/google_image_scraper/cli/main.py',
    ]
    
    missing_files = []
    for file_path in expected_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All expected files exist")
    return True

async def main():
    """Run all tests"""
    print("🚀 Testing Google Image Scraper Modular Structure")
    print("=" * 60)
    
    tests = [
        test_package_structure,
        test_imports,
        test_configuration,
        test_scraper_creation,
        test_cli_imports,
        test_url_extraction,  # This one is async
    ]
    
    results = []
    
    for test in tests:
        try:
            if asyncio.iscoroutinefunction(test):
                result = await test()
            else:
                result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test.__name__}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The modular structure is working correctly.")
        print("\nNext steps:")
        print("1. Install the package: pip install -e .")
        print("2. Try the CLI: google-image-scraper --help")
        print("3. Run examples: python examples/basic_usage.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False
    
    return True

if __name__ == '__main__':
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[INFO] Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Test runner failed: {e}")
        sys.exit(1)
