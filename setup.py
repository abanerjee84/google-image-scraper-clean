#!/usr/bin/env python3
"""
Setup script for Google Image Scraper
"""
import subprocess
import sys
import os
from pathlib import Path


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


def install_dependencies():
    """Install Python dependencies"""
    commands = [
        ("pip install -r requirements.txt", "Installing core dependencies"),
        ("playwright install", "Installing Playwright browsers")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def install_dev_dependencies():
    """Install development dependencies"""
    if Path("requirements-dev.txt").exists():
        return run_command("pip install -r requirements-dev.txt", "Installing development dependencies")
    return True


def create_directories():
    """Create necessary directories"""
    directories = ["photos", "google_search", "logs"]
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print(f"✅ Created directory: {directory}")
        except Exception as e:
            print(f"❌ Failed to create directory {directory}: {e}")
            return False
    
    return True


def verify_installation():
    """Verify that the installation works"""
    print("🔍 Verifying installation...")
    
    try:
        # Try importing main modules
        import playwright
        import httpx
        import PIL
        print("✅ All core modules can be imported")
        
        # Check if Playwright browsers are installed
        result = subprocess.run(
            ["python", "-c", "from playwright.sync_api import sync_playwright; sync_playwright().start()"],
            capture_output=True, text=True, timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Playwright browsers are installed and working")
        else:
            print("⚠️  Warning: Playwright browsers may not be properly installed")
            print("   You may need to run: playwright install")
        
        return True
        
    except ImportError as e:
        print(f"❌ Module import failed: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  Playwright verification timed out")
        return True  # Don't fail the setup for this
    except Exception as e:
        print(f"⚠️  Verification warning: {e}")
        return True  # Don't fail the setup for warnings


def main():
    """Main setup function"""
    print("🚀 Google Image Scraper Setup")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Install dependencies
    if success and not install_dependencies():
        success = False
    
    # Create directories
    if success and not create_directories():
        success = False
    
    # Verify installation
    if success:
        verify_installation()
    
    print("\n" + "=" * 50)
    
    if success:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit search terms in main.py or use the CLI:")
        print("   python cli.py cats dogs --count 10")
        print("2. Run the scraper:")
        print("   python main.py")
        print("3. Check the 'photos' folder for downloaded images")
        
        # Check if development dependencies should be installed
        if input("\nInstall development dependencies? (y/N): ").lower().startswith('y'):
            install_dev_dependencies()
    else:
        print("❌ Setup failed. Please check the errors above and try again.")
        print("\nTroubleshooting:")
        print("- Make sure you have Python 3.8+ installed")
        print("- Try upgrading pip: python -m pip install --upgrade pip")
        print("- Check your internet connection")
        sys.exit(1)


if __name__ == "__main__":
    main()
