# Telegram Movie Bot

A production-ready Telegram Movie Bot built with Python, Pyrogram, and SQLite.

## Features
- 🎬 Fast inline and text search for movies
- 📢 Force join channel verification
- 📥 Direct file downloads via `file_id`
- 📊 Admin commands (`/stats`, `/broadcast`, `/addmovie`, `/delmovie`)
- 🗄️ SQLite database for fast queries
- 🤖 Auto-add movies from a private storage channel

## Setup Instructions

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Copy `.env.example` to `.env` and fill in your details:
   ```bash
   cp .env.example .env
   ```
   - `API_ID` and `API_HASH`: Get from [my.telegram.org](https://my.telegram.org)
   - `BOT_TOKEN`: Get from [@BotFather](https://t.me/BotFather)
   - `ADMIN_ID`: Your Telegram User ID
   - `FORCE_JOIN_CHANNEL`: Public channel username (e.g., `@mychannel`)
   - `STORAGE_CHANNEL`: Private channel ID (e.g., `-1001234567890`)

4. **Run the bot**
   ```bash
   python bot.py
   ```

## How to Add Movies

**Method 1: Auto-add via Storage Channel**
1. Add the bot as an admin to your private `STORAGE_CHANNEL`.
2. Upload a movie file (document or video) to the channel.
3. Set the caption exactly like this:
   `Movie Name | Year | Language | Quality`
   *(Example: `Inception | 2010 | English | 1080p`)*
4. The bot will automatically save it to the database.

**Method 2: Manual add via Bot**
1. Send the movie file to the bot in private chat.
2. Reply to the file with the command:
   `/addmovie Movie Name | Year | Language | Quality`
