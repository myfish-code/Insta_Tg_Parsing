import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
CHANNEL_ID = os.getenv("CHANNEL_ID")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
CHANNEL_LINK = os.getenv("CHANNEL_LINK")
LOGIN_INST = os.getenv("LOGIN_INST")
PASSWORD_INST = os.getenv("PASSWORD_INST")
PROXY_URL = os.getenv("PROXY_URL")

admin_ids_str = os.getenv("ADMINS", "")
ADMINS = [int(admin_id.strip()) for admin_id in admin_ids_str.split(",") if admin_id.strip()]

PAGE_SIZE = 5
MAX_TAKEN = 5
LIMIT_POSTS = 3
