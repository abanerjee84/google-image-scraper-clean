#!/usr/bin/env python3
"""
Installation and setup script for the new modular Google Image Scraper
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description, cwd=None):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        print(f"   Output: {e.stdout}")
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

def create_virtual_environment():
    """Create a virtual environment for the project"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("ℹ️  Virtual environment already exists")
        return True
    
    return run_command(f"{sys.executable} -m venv venv", "Creating virtual environment")

def install_package():
    """Install the package in development mode"""
    # Determine the correct pip command based on OS
    if os.name == 'nt':  # Windows
        pip_cmd = r"venv\Scripts\pip"
        python_cmd = r"venv\Scripts\python"
    else:  # Unix/Linux/MacOS
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    commands = [
        (f"{pip_cmd} install --upgrade pip", "Upgrading pip"),
        (f"{pip_cmd} install -e .", "Installing package in development mode"),
        (f"{python_cmd} -m playwright install", "Installing Playwright browsers"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def test_installation():
    """Test that the installation worked"""
    print("\n🧪 Testing installation...")
    
    # Determine the correct python command
    if os.name == 'nt':  # Windows
        python_cmd = r"venv\Scripts\python"
    else:  # Unix/Linux/MacOS
        python_cmd = "venv/bin/python"
    
    test_commands = [
        (f"{python_cmd} -c \"from google_image_scraper import GoogleImageScraper; print('✅ Package import successful')\"", 
         "Testing package import"),
        (f"{python_cmd} -c \"from google_image_scraper.cli.main import create_parser; print('✅ CLI import successful')\"", 
         "Testing CLI import"),
        (f"{python_cmd} -m google_image_scraper --help", 
         "Testing CLI command"),
    ]
    
    for command, description in test_commands:
        if not run_command(command, description):
            return False
    
    return True

def create_activation_scripts():
    """Create convenient activation scripts"""
    
    # Windows batch file
    windows_script = """@echo off
echo Activating Google Image Scraper environment...
call venv\\Scripts\\activate.bat
echo.
echo Environment activated! You can now use:
echo   - google-image-scraper cats --count 10
echo   - gis cats --count 10
echo   - python -m google_image_scraper cats --count 10
echo   - python examples/basic_usage.py
echo.
echo Type 'deactivate' to exit the environment.
cmd /k
"""
    
    # Unix shell script
    unix_script = """#!/bin/bash
echo "Activating Google Image Scraper environment..."
source venv/bin/activate
echo ""
echo "Environment activated! You can now use:"
echo "  - google-image-scraper cats --count 10"
echo "  - gis cats --count 10"
echo "  - python -m google_image_scraper cats --count 10"
echo "  - python examples/basic_usage.py"
echo ""
echo "Type 'deactivate' to exit the environment."
exec "$SHELL"
"""
    
    try:
        # Create Windows activation script
        with open("activate_env.bat", "w") as f:
            f.write(windows_script)
        print("✅ Created activate_env.bat for Windows")
        
        # Create Unix activation script
        with open("activate_env.sh", "w") as f:
            f.write(unix_script)
        
        # Make Unix script executable
        os.chmod("activate_env.sh", 0o755)
        print("✅ Created activate_env.sh for Unix/Linux/MacOS")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create activation scripts: {e}")
        return False

def show_usage_examples():
    """Show usage examples"""
    print("\n🎯 USAGE EXAMPLES")
    print("=" * 50)
    
    print("\n1. Command Line Usage:")
    print("   google-image-scraper cats dogs --count 10 --headless")
    print("   gis 'red roses' --min-res 800x600 --format png")
    print("   python -m google_image_scraper cats --dry-run")
    
    print("\n2. Python Usage:")
    print("""   from google_image_scraper import GoogleImageScraper
   scraper = GoogleImageScraper()
   urls, count = await scraper.scrape('cats')""")
    
    print("\n3. Run Examples:")
    print("   python examples/basic_usage.py")
    
    print("\n4. Activate Environment:")
    if os.name == 'nt':
        print("   activate_env.bat")
    else:
        print("   ./activate_env.sh")

def main():
    """Main installation process"""
    print("🚀 Google Image Scraper - Modular Installation")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    print("\n📦 Setting up development environment...")
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        return False
    
    # Install package and dependencies
    if not install_package():
        print("❌ Failed to install package")
        return False
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        return False
    
    # Create activation scripts
    create_activation_scripts()
    
    print("\n🎉 INSTALLATION SUCCESSFUL!")
    print("=" * 60)
    
    show_usage_examples()
    
    print("\n📝 Next Steps:")
    print("1. Activate the environment:")
    if os.name == 'nt':
        print("   activate_env.bat")
    else:
        print("   ./activate_env.sh")
    print("2. Test the CLI: google-image-scraper --help")
    print("3. Run examples: python examples/basic_usage.py")
    print("4. Start scraping: google-image-scraper cats --count 5")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[INFO] Installation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Installation failed: {e}")
        sys.exit(1)
