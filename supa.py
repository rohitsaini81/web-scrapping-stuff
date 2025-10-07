import os
from supabase import create_client, Client


from dotenv import load_dotenv
from Logger import logger

# Load environment variables
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_supa():
    response = (
            supabase.table("videos")
            .select("*")
            .execute()
            )
    return response

video_data = {
    "title": "Exploring the Mountains",
    "description": "A travel vlog showcasing the scenic mountain ranges.",
    "category": "Travel",
    "tags": ["nature", "adventure", "vlog"],
    "duration": "12:45",
    "img_url": "https://example.com/images/mountains.jpg",
    "video_url": "https://example.com/videos/mountains.mp4",
    "image": True,
    "video": True
}



def insert_supa(data):
    response = (
            supabase.table("videos")
            .insert(data)
            .execute())
    return response


response = (
        supabase.table("videos")
        .select()
        .count("*")
        .execute())
print(response)


