import os
from supabase import create_client, Client


from dotenv import load_dotenv
from Logger import logger

# Load environment variables
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


response = (
    supabase.table("videos")
    .select("*")
    .execute()
)

print(response)
