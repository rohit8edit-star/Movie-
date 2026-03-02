import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from database import db
from config import ADMIN_ID

def is_admin(func):
    async def wrapper(client, message):
        if message.from_user.id != ADMIN_ID:
            return
        return await func(client, message)
    return wrapper

@Client.on_message(filters.command("stats") & filters.private)
@is_admin
async def stats_command(client, message):
    total_users = db.get_total_users()
    await message.reply_text(f"📊 **Bot Statistics**\n\n👥 Total Users: {total_users}")

@Client.on_message(filters.command("broadcast") & filters.private)
@is_admin
async def broadcast_command(client, message):
    if not message.reply_to_message:
        await message.reply_text("Please reply to a message to broadcast it.")
        return

    users = db.get_all_users()
    msg = await message.reply_text(f"Broadcasting to {len(users)} users...")
    
    success = 0
    failed = 0
    
    for user_id in users:
        try:
            await message.reply_to_message.copy(user_id)
            success += 1
            await asyncio.sleep(0.05) # Prevent FloodWait
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(user_id)
            success += 1
        except Exception:
            failed += 1

    await msg.edit_text(f"✅ **Broadcast Completed**\n\n✅ Success: {success}\n❌ Failed: {failed}")

@Client.on_message(filters.command("addmovie") & filters.private)
@is_admin
async def add_movie_command(client, message):
    # Format: /addmovie Name | Year | Language | Quality
    # Must reply to a file
    if not message.reply_to_message or not (message.reply_to_message.document or message.reply_to_message.video):
        await message.reply_text("Please reply to a document or video to add a movie.")
        return

    try:
        args = message.text.split(" ", 1)[1]
        name, year, lang, quality = [x.strip() for x in args.split("|")]
        year = int(year)
    except Exception:
        await message.reply_text("❌ Invalid format.\nUsage: `/addmovie Name | Year | Language | Quality` (reply to file)")
        return

    file_id = message.reply_to_message.document.file_id if message.reply_to_message.document else message.reply_to_message.video.file_id
    
    db.add_movie(name, year, lang, quality, file_id)
    await message.reply_text(f"✅ Movie **{name}** added successfully!")

@Client.on_message(filters.command("delmovie") & filters.private)
@is_admin
async def del_movie_command(client, message):
    try:
        movie_id = int(message.text.split(" ")[1])
    except Exception:
        await message.reply_text("❌ Invalid format.\nUsage: `/delmovie <movie_id>`")
        return

    movie = db.get_movie_by_id(movie_id)
    if not movie:
        await message.reply_text("❌ Movie not found.")
        return

    db.delete_movie(movie_id)
    await message.reply_text(f"✅ Movie ID {movie_id} deleted successfully.")
