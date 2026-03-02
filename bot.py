import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if not all([API_ID, API_HASH, BOT_TOKEN]):
    logger.error("Please set API_ID, API_HASH, and BOT_TOKEN in .env file.")
    exit(1)

app = Client(
    "movie_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

if __name__ == "__main__":
    logger.info("Bot is starting...")
    app.run()
