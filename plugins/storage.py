from pyrogram import Client, filters
from database import db
from config import STORAGE_CHANNEL

@Client.on_message(filters.chat(STORAGE_CHANNEL) & (filters.document | filters.video))
async def auto_add_movie(client, message):
    # Expected caption format: Name | Year | Language | Quality
    if not message.caption:
        return
        
    try:
        name, year, lang, quality = [x.strip() for x in message.caption.split("|")]
        year = int(year)
    except Exception:
        # Invalid format, ignore
        return

    file_id = message.document.file_id if message.document else message.video.file_id
    
    db.add_movie(name, year, lang, quality, file_id)
    print(f"Auto-added movie: {name} ({year})")
