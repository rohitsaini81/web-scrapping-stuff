import boto3
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Cloudflare R2
s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('R2_ENDPOINT'),
    aws_access_key_id=os.getenv('R2_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('R2_SECRET_KEY'),
)

def download_file_temp(url, save_path):
    """Downloads a file from a given URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"✅ File downloaded: {save_path}")
        return save_path
    except Exception as e:
        print(f"❌ Download error: {e}")
        return None

def upload_file(file_path):
    """Uploads a file to Cloudflare R2 and deletes it after upload."""
    try:
        bucket_name = os.getenv('R2_BUCKET_NAME')
        file_name = os.path.basename(file_path)

        # Upload file
        s3_client.upload_file(file_path, bucket_name, file_name)

        # Generate Public URL
        file_url = f"https://https://pub-a919e0e7442047299d7072ac1b2ab5d0.r2.dev/{file_name}"
        # print(f"📌 File URL: {file_url}")

        # Delete file after upload
        os.remove(file_path)
        print(f"🗑️ File deleted: {file_path}")

        return file_name
    except Exception as e:
        print(f"❌ Upload error: {e}")

# Example Usage
# file_url = 'https://videos.pexels.com/video-files/3196174/3196174-uhd_2560_1440_25fps.mp4'  
# save_path = "/tmp/temp_video.mp4"  # Save location

# downloaded_file = download_file(file_url, save_path)
# if downloaded_file:
#     upload_file(downloaded_file)
