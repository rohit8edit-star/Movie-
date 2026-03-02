import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

def parse_channel(val):
    if not val:
        return ""
    try:
        return int(val)
    except ValueError:
        return val

FORCE_JOIN_CHANNEL = parse_channel(os.getenv("FORCE_JOIN_CHANNEL", ""))
STORAGE_CHANNEL = parse_channel(os.getenv("STORAGE_CHANNEL", ""))
