import boto3
import os
from dotenv import load_dotenv
from Logger import logger

# Load environment variables
load_dotenv()

# Configure Cloudflare R2
s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('R2_ENDPOINT'),
    aws_access_key_id=os.getenv('R2_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('R2_SECRET_KEY'),
)

def upload_file(file_path):
    """Uploads a file to Cloudflare R2"""
    try:
        bucket_name = os.getenv('R2_BUCKET_NAME')
        
        # Extract filename from path
        file_name = os.path.basename(file_path)

        # Upload file
        s3_client.upload_file(file_path, bucket_name, file_name, ExtraArgs={'ContentType': 'image/png'})

        # Generate Public URL
        file_url = f"https://{bucket_name}.{os.getenv('R2_ENDPOINT').replace('https://', '')}/{file_name}"
        logger.info(f"✅ File uploaded successfully: {file_name}")
        logger.info(f"📌 File URL: {file_url}")
        return file_url
    except Exception as e:
        logger.info(f"❌ Upload error: {e}")

# Example Usage
file_path = 'https://videos.pexels.com/video-files/3196174/3196174-uhd_2560_1440_25fps.mp4'  # Replace with your file path

upload_file(file_path)
