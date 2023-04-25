import telegram
from telegram.ext import ContextTypes, ConversationHandler


async def cancel(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    """Cancels and ends the conversation."""
    update.message.reply_text(text="cancelled.")

    return ConversationHandler.END
