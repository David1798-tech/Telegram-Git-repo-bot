from functools import wraps
from config import ALLOWED_USER_IDS


def restricted(func):
    """Only allow whitelisted Telegram user IDs. Skip check if list is empty."""
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        if ALLOWED_USER_IDS:
            user_id = update.effective_user.id
            if user_id not in ALLOWED_USER_IDS:
                await update.message.reply_text("⛔ Unauthorized.")
                return
        return await func(update, context, *args, **kwargs)
    return wrapper
