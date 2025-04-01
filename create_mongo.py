import os
from pymongo import MongoClient
from dotenv import load_dotenv
from Logger import logger

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE = os.getenv("DATABASE")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Connect to MongoDB (forcing IPv4 for compatibility)
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")  # Test connection
    logger.info("Connected to MongoDB Atlas")
except Exception as e:
    logger.info("Connection failed:", e)
    exit(1)

db = client[DATABASE]
collection = db[COLLECTION_NAME]
                                                                             # Write Data
def insert_document(title, img_url, video_url, tags, description, category, duration):
    new_data = {
        "title": title,
        "img_url": img_url,
        "video_url": video_url,
        "tags": tags,  # Array of tags
        "description": description,
        "category": category,
        "duration": duration
    }
    insert_result = collection.insert_one(new_data)
    logger.info("Inserted document ID:", insert_result.inserted_id)

# Read All Documents
def read_all_documents():
    documents = collection.find()  # Retrieve all documents
    for doc in documents:
        logger.info(doc)

# Example Usage

# Insert a new document
# insert_document(
#    title="New Video",
#    img_url="https://example.com/image.jpg",
#    video_url="https://example.com/video.mp4",
#     tags=["AI", "Machine Learning", "Python"],
#     description="This is a tutorial on AI with Python.",
#     category="Education",
#     duration=120  # Duration in minutes
# )

# Read all documents
# read_all_documents()

# Close Connection
# client.close()
