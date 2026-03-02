from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database import db
from utils import check_force_join, get_force_join_markup

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    user_id = message.from_user.id
    db.add_user(user_id)
    
    if not await check_force_join(client, user_id):
        await message.reply_text(
            "👋 Hello! To use this bot, you must join our updates channel first.",
            reply_markup=get_force_join_markup()
        )
        return

    welcome_text = (
        "🎬 **Welcome to the Movie Bot!**\n\n"
        "I can help you find and download movies easily.\n"
        "Just send me the name of the movie you want to watch!"
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔎 Search Movie", switch_inline_query_current_chat="")],
        [
            InlineKeyboardButton("📂 Categories", callback_data="categories"),
            InlineKeyboardButton("🔥 Trending", callback_data="trending")
        ],
        [InlineKeyboardButton("🆘 Help", callback_data="help")]
    ])
    
    await message.reply_text(welcome_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("^check_join$"))
async def check_join_callback(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if await check_force_join(client, user_id):
        await callback_query.message.delete()
        await start_command(client, callback_query.message)
    else:
        await callback_query.answer("You haven't joined the channel yet!", show_alert=True)

@Client.on_callback_query(filters.regex("^(categories|trending|help)$"))
async def basic_callbacks(client, callback_query: CallbackQuery):
    data = callback_query.data
    if data == "help":
        await callback_query.answer("Send me a movie name to search. Use /start to see the menu.", show_alert=True)
    else:
        await callback_query.answer("This feature is coming soon!", show_alert=True)
