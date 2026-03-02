from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database import db
from utils import check_force_join, get_force_join_markup

@Client.on_message(filters.text & filters.private & ~filters.command(["start", "stats", "broadcast", "addmovie", "delmovie"]))
async def search_movie(client, message):
    user_id = message.from_user.id
    
    if not await check_force_join(client, user_id):
        await message.reply_text(
            "You must join our channel to search for movies.",
            reply_markup=get_force_join_markup()
        )
        return

    query = message.text
    if len(query) < 2:
        await message.reply_text("Please enter at least 2 characters to search.")
        return

    results = db.search_movie(query)

    if not results:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Request Movie", callback_data=f"req_{query[:40]}")]
        ])
        await message.reply_text(f"❌ No movies found for **{query}**.", reply_markup=keyboard)
        return

    # Group by movie name and year
    movies = {}
    for row in results:
        m_id, name, year, lang, quality, file_id = row
        key = f"{name.title()} ({year})"
        if key not in movies:
            movies[key] = []
        movies[key].append((m_id, lang, quality))

    for movie_title, files in movies.items():
        text = f"🎬 **{movie_title}**\n\n**Available Qualities:**\n"
        buttons = []
        for m_id, lang, quality in files:
            text += f"• {quality} - {lang}\n"
            buttons.append([InlineKeyboardButton(f"📥 Download {quality} ({lang})", callback_data=f"dl_{m_id}")])
        
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex(r"^dl_(\d+)$"))
async def download_movie(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if not await check_force_join(client, user_id):
        await callback_query.message.reply_text(
            "You must join our channel to download movies.",
            reply_markup=get_force_join_markup()
        )
        return

    movie_id = int(callback_query.matches[0].group(1))
    movie = db.get_movie_by_id(movie_id)
    
    if not movie:
        await callback_query.answer("Movie not found in database.", show_alert=True)
        return

    _, name, year, lang, quality, file_id = movie
    
    try:
        await client.send_document(
            chat_id=user_id,
            document=file_id,
            caption=f"🎬 **{name.title()} ({year})**\n📀 {quality} | 🔊 {lang}\n\nDownloaded via @{client.me.username}"
        )
        await callback_query.answer("Sending file...")
    except Exception as e:
        print(f"Error sending file: {e}")
        await callback_query.answer("Error sending file. It might have been deleted.", show_alert=True)

@Client.on_callback_query(filters.regex(r"^req_(.+)$"))
async def request_movie(client, callback_query: CallbackQuery):
    movie_name = callback_query.matches[0].group(1)
    user_id = callback_query.from_user.id
    db.add_request(user_id, movie_name)
    await callback_query.answer("✅ Your request has been submitted!", show_alert=True)
    await callback_query.message.edit_text(f"✅ Request for **{movie_name}** has been recorded.")
