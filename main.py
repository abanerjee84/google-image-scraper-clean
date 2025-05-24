import os
import asyncio
from GoogleImageScraper import find_image_urls, save_images, save_urls_to_json

async def scrape_task(
        search_key: str,
        number_of_images: int,
        max_missed: int,
        headless: bool,
        min_resolution,
        max_resolution,
        keep_filenames,
    ):
    print(f'[INFO] Starting scrape task for: {search_key}')
    image_urls = await find_image_urls(
        search_key,
        number_of_images,
        max_missed,
        headless
    )
    
    print(f'[INFO] Found {len(image_urls)} URLs for {search_key}, now downloading images...')
    await save_images(
        image_urls,
        image_save_format='jpg',
        images_dir_path=os.path.join('photos', search_key),
        keep_filenames=keep_filenames,
        image_file_prefix=search_key,
        min_resolution=min_resolution,
        max_resolution=max_resolution
    )
    print(f'[INFO] Completed scrape task for: {search_key}')

#Run each search_key in a separate async task
async def main():
    #Define file path
    images_dir_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    #Removes duplicate strings from search_keys
    #Add new search key into array ['cat','t-shirt','apple','orange','pear','fish']
    search_keys = list(set(['lettuce', 'spinach']))

    #Parameters
    number_of_images = 10                # Desired number of images
    min_resolution = (0, 0)             # Minimum desired image resolution
    max_resolution = (9999, 9999)       # Maximum desired image resolution
    max_missed = 10                     # Max number of failed images before exit
    headless = True                     # True = No Chrome GUI
    number_of_workers = 1               # Number of workers used
    keep_filenames = False              # Keep original URL image filenames

    try:
        tasks = [
            scrape_task(
                search_key,
                number_of_images,
                max_missed,
                headless,
                min_resolution,
                max_resolution,
                keep_filenames
            ) for search_key in search_keys
        ]
        # waits for all tasks to finish
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    except Exception as e:
        print(f"[ERROR] An error occurred during scraping: {e}")
        return None

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[INFO] Script interrupted by user")
    except Exception as e:
        print(f"[ERROR] Script failed with error: {e}")
    finally:
        # Ensure all async resources are cleaned up
        try:
            loop = asyncio.get_event_loop()
            if not loop.is_closed():
                # Cancel all running tasks
                pending = asyncio.all_tasks(loop)
                for task in pending:
                    task.cancel()
                # Wait for all tasks to complete cancellation
                if pending:
                    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except RuntimeError:
            # Event loop is already closed
            pass
