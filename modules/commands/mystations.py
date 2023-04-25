import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from modules.wrappers import Sqlite
from tabulate import tabulate


async def mystations(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db = Sqlite('meteo.db')
    chatid = int(update.message.chat_id)
    user_rivers = db.read_user_rivers(chatid=chatid)
    
    header = ("River/Lake", "Threshold Lvl.")
    print(user_rivers)
    table = tabulate(user_rivers,headers=header)
    table = "``` Current watchlist:\n\n" + table + "```"
    
    await update.message.reply_text(text=table,parse_mode="MarkdownV2")
    
command = CommandHandler("mystations",mystations)