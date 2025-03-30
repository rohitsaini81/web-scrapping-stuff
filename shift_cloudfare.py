import boto3
import os
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

def move_file(source_bucket, destination_bucket, file_key):
    """Moves a file from one R2 bucket to another."""
    try:
        # Copy the file to the destination bucket
        copy_source = {'Bucket': source_bucket, 'Key': file_key}
        s3_client.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=file_key)
        print(f"✅ File copied to {destination_bucket}/{file_key}")

        # Delete the file from the source bucket
        s3_client.delete_object(Bucket=source_bucket, Key=file_key)
        print(f"🗑️ File deleted from {source_bucket}/{file_key}")

    except Exception as e:
        print(f"❌ Error: {e}")

# Example usage
source_bucket = "stream"
destination_bucket = "videos"
file_key = "Kooha-2025-03-14-22-46-43.mp4"  # Replace with your actual file key




# thats simple read from videos and then shifts to videos
# move_file(source_bucket, destination_bucket, file_key)

# List all files in the source bucket
from create import read_videos

def list_files_in_bucket():
    data = read_videos()
    for video in data:
        video_id = video[0]
        video_url = video[1]
        img_url = video[2]
        print(f"Video ID: {video_id}, Video URL: {video_url}, Image URL: {img_url}")
        move_file(source_bucket, destination_bucket, video_url)

    



list_files_in_bucket()