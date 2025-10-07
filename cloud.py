
import boto3
from botocore.client import Config
from Logger import logger

# Replace with your actual credentials and bucket details
ACCESS_KEY = "87e10a56324c3eb98427d14d6de6b90a"
SECRET_KEY = "080eb45e8007ee4e33cd11b0157e58411fd9dd9fc22e7cf7e08cd646adca1963"
ENDPOINT_URL = "https://b3ecced75c39787365b3063e12596605.r2.cloudflarestorage.com"
BUCKET_NAME = "videos"  # Replace with your actual bucket name
VIDEO_FILE_PATH = "video.mp4"  # Replace with your actual video file path

# Initialize the S3 client with R2 credentials
s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT_URL,  # Cloudflare R2 endpoint
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version="s3v4"),
)

def upload_video(file_path, bucket_name, object_name=None):
    """Uploads a video file to Cloudflare R2."""
    if object_name is None:
        object_name = file_path.split("/")[-1]  # Use the filename as the object name

    try:
        with open(file_path, "rb") as file:
            s3.upload_fileobj(file, bucket_name, object_name)
        logger.info(f"Upload successful: {object_name} → {bucket_name}")
        logger.info(f"Access URL: {ENDPOINT_URL}/{bucket_name}/{object_name}")
    except Exception as e:
        logger.info("Error uploading file:", e)




def delete_video(file_name, bucket_name):

    paginator = s3.get_paginator('list_objects_v2')
    deleted_count = 0
    
    for page in paginator.paginate(Bucket=bucket_name):
        if 'Contents' not in page:
            print("Bucket is already empty.")
            return

        objects_to_delete = [{'Key': obj['Key']} for obj in page['Contents']]


        #print(page.key)
        response = s3.delete_objects(
            Bucket=bucket_name,
            Delete={'Objects': objects_to_delete}
        )

        deleted = len(response.get('Deleted', []))
        deleted_count += deleted
        print(f"Deleted {deleted} objects from bucket...")

    print(f"✅ Finished — total deleted: {deleted_count}")
    return "ok"




delete_video("a", "videos")
# Upload the video
# upload_video(VIDEO_FILE_PATH, BUCKET_NAME)

