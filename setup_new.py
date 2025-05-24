#!/usr/bin/env python3
"""
Setup script for Google Image Scraper - Professional Package
"""
from setuptools import setup, find_packages
import subprocess
import sys
import os
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
def read_requirements(filename):
    """Read requirements from file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

requirements = read_requirements('requirements.txt')
dev_requirements = read_requirements('requirements-dev.txt')

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_playwright_browsers():
    """Install Playwright browsers"""
    return run_command("playwright install", "Installing Playwright browsers")

def install_dependencies():
    """Install Python dependencies"""
    commands = [
        ("pip install -e .", "Installing package in development mode"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    # Install Playwright browsers
    return install_playwright_browsers()

# Setup configuration
setup(
    name="google-image-scraper",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A professional Python package for scraping Google Images with advanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abanerjee84/google-image-scraper-clean",
    project_urls={
        "Bug Tracker": "https://github.com/abanerjee84/google-image-scraper-clean/issues",
        "Documentation": "https://github.com/abanerjee84/google-image-scraper-clean#readme",
        "Source Code": "https://github.com/abanerjee84/google-image-scraper-clean",
    },
    
    # Package configuration
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Dependencies
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
    
    # Entry points for CLI
    entry_points={
        "console_scripts": [
            "google-image-scraper=google_image_scraper.cli.main:main",
            "gis=google_image_scraper.cli.main:main",  # Short alias
        ],
    },
    
    # Metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Keywords
    keywords=[
        "google", "images", "scraper", "download", "automation", 
        "web-scraping", "playwright", "image-processing"
    ],
    
    # Include additional files
    include_package_data=True,
    package_data={
        "google_image_scraper": ["py.typed"],
    },
    
    # Project is typed
    zip_safe=False,
)

def main():
    """Main setup function"""
    print("🚀 Google Image Scraper Setup")
    print("=" * 50)
    
    if not check_python_version():
        sys.exit(1)
    
    print("\n📦 Installing package and dependencies...")
    if not install_dependencies():
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nYou can now use the scraper in several ways:")
    print("1. Command line: google-image-scraper cats dogs --count 10")
    print("2. Short alias: gis cats dogs --count 10")
    print("3. Python import: from google_image_scraper import GoogleImageScraper")
    print("4. Run examples: python examples/basic_usage.py")

if __name__ == "__main__":
    main()
