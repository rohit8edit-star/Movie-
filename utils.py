from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_JOIN_CHANNEL

async def check_force_join(client, user_id):
    if not FORCE_JOIN_CHANNEL:
        return True
    try:
        member = await client.get_chat_member(FORCE_JOIN_CHANNEL, user_id)
        if member.status.value in ["kicked", "left", "banned"]:
            return False
        return True
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Error checking force join: {e}")
        # If bot is not admin in the channel, it might throw an error.
        return False

def get_force_join_markup():
    channel_link = str(FORCE_JOIN_CHANNEL)
    if channel_link.startswith("-100"):
        # We can't link directly to private ID without invite link, 
        # so it's better if FORCE_JOIN_CHANNEL is a public username like @channel
        url = "https://t.me/telegram" # Fallback
    else:
        url = f"https://t.me/{channel_link.replace('@', '')}"
        
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel", url=url)],
        [InlineKeyboardButton("🔄 Check Again", callback_data="check_join")]
    ])
