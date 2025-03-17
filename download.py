import os
import hashlib
import requests
from urllib.parse import urlparse
from create import *


def get_unique_filename(url, folder="../public/downloads"):
    """Generates a unique filename based on URL"""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    print(filename)

    # Ensure the directory exists
    os.makedirs(folder, exist_ok=True)

    # Generate a hash of the URL
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]  # 8-char unique hash

    # Check if file exists, if yes, append hash
    unique_filename = f"{filename}_{url_hash}" if os.path.exists(
        os.path.join(folder, filename)) else filename
    return os.path.join(folder, unique_filename)


def download_file(url, isImage=False):
    """Downloads a file and saves it with a unique name"""
    filename = get_unique_filename(url)
    parsed_url = urlparse(url)
    if not parsed_url.scheme:  # No 'http' or 'https' in URL
        print(f"Invalid URL: {url}")
        return
    if update_url(url, filename, isImage):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {filename}")

        else:
            print(f"Failed to download: {url}")
    else:
        print("no not you")


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
        print("Error: No data to process.")
    else:
        for row in maindata:
            try:
                print(row[3])
                print(count)
                count += 1
                download_file(row[3])
            except Exception as e:
                print(f"Error processing row: {row}, Error: {e}")
                continue
