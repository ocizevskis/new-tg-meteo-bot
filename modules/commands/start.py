import telegram
from telegram.ext import CommandHandler, ContextTypes


async def hello(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update)
    await update.message.reply_text(text="use /add to add your first station to watchlist, or /get to get a specific station's water level")
    

command = CommandHandler("start",hello)