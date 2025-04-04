import os
import hashlib
import requests
from urllib.parse import urlparse
from create import *
import time
from Logger import logger



import os

def is_file_valid(filename, min_size=1000):
    """Check if the downloaded file is valid by size."""
    return os.path.exists(filename) and os.path.getsize(filename) > min_size




def get_unique_filename(url, folder="downloads"):
    """Generates a unique filename based on URL"""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # Ensure the directory exists
    os.makedirs(folder, exist_ok=True)

    # Generate a hash of the URL
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]  # 8-char unique hash

    # Check if file exists, if yes, append hash
    unique_filename = f"{filename}_{url_hash}" if os.path.exists(
        os.path.join(folder, filename)) else filename
    return os.path.join(folder, unique_filename)





def download_file(url, isImage, max_retries=3):
    """Downloads a file and saves it with a unique name, retrying on failures."""
    filename = get_unique_filename(url)
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        logger.info(f"Invalid URL: {url}")
        return

    logger.info("url: " + url)
    
    if update_url(url, filename, isImage):
        for attempt in range(max_retries):
            try:
                
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

                response = requests.get(url, headers=headers, stream=True , timeout=10, verify=False)

                if response.status_code == 200:
                    with open(filename, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    # After download:
                    if is_file_valid(filename):
                        logger.info(f"Successfully downloaded: {filename}")
                    else:
                        logger.info(f"Download failed or file is corrupt: {filename}")


                    return  # Exit function on success
                else:
                    logger.info(f"Failed to download ({response.status_code}): {url}")
            except requests.exceptions.RequestException as e:
                logger.info(f"Error downloading {url}: {e}")
            
            logger.info(f"Retrying ({attempt + 1}/{max_retries})...")
            time.sleep(2)  # Wait before retrying

        logger.info(f"Failed after {max_retries} attempts: {url}")
    else:
        logger.info("No update required.")








def downloads(url, isImage, max_retries=3, timeout=10):
    """Downloads a file and saves it with a unique name, retrying on failures."""
    filename = get_unique_filename(url)
    
    # Validate URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        logger.info(f"Invalid URL: {url}")
        return False
    
    
    logger.info(f"Downloading: {url} -> {filename}")

    # Request headers to avoid blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=timeout, verify=False)

            if response.status_code == 200:
                with open(filename, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)

                # Check file size to ensure it's not empty
                if os.path.exists(filename) and os.path.getsize(filename) > 0:
                    logger.info(f"✅ Successfully downloaded: {filename}")
                # uploading to cloudflare
                    return filename  # Success
                else:
                    logger.info(f"⚠️ Empty file detected: {filename}")
                    os.remove(filename)  # Delete 0-byte file
            
            else:
                logger.info(f"❌ Failed (Status: {response.status_code}): {url}")

        except requests.exceptions.RequestException as e:
            logger.info(f"⚠️ Attempt {attempt}/{max_retries} failed: {e}")
        
        time.sleep(2)  # Wait before retrying

    logger.info(f"❌ All retries failed for: {url}")
    return False  # Failed after retries
  



# Example URLs (Replace with real scraped URLs)
urls = [
    "https://www.hotxv.com/thumbs/xv/med/gd4ll3k8nnd.jpg",
    "https://www.hotxv.com/thumbs/xv/med/gd537170ddd.jpg",
    "https://www.hotxv.com/thumbs/xv/med/7ej3e9kjpwk.jpg",
    "https://www.hotxv.com/thumbs/xv/med/7ekl675zkfk.jpg",
]

# Download each file
# for url in urls:
# download_file(url)


def download_link():

    maindata = read_videos()
    count = 0

    if maindata is None:
        logger.info("Error: No data to process.")
    else:
        for row in maindata:
            try:
                logger.info(row[3])
                logger.info(count)
                count += 1
                # download_file(row[3])
            except Exception as e:
                logger.info(f"Error processing row: {row}, Error: {e}")
                continue
