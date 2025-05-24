"""
Entry point for running the CLI when the package is executed as a module
Usage: python -m google_image_scraper
"""
import asyncio
import sys

def main():
    """Main entry point for the module"""
    try:
        from .cli.main import main as cli_main
        asyncio.run(cli_main())
    except KeyboardInterrupt:
        print("\n[INFO] Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Script failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
