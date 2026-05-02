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

PAGE_SIZE = 5
MAX_TAKEN = 10
LIMIT_POSTS = 1