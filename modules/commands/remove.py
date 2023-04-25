import telegram
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from modules.wrappers import Sqlite


async def remove(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    rivers = Sqlite('meteo.db').read_user_rivers(chatid=update.message.chat_id)
    buttons = [[telegram.KeyboardButton(text=str(i[0])) ]for i in rivers]
    test = telegram.ReplyKeyboardMarkup(keyboard=buttons,one_time_keyboard=True)
    await update.message.reply_text(reply_markup=test,text="Choose the appropriate station")
    
    return 0


async def remove_done(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chatid = update.message.chat_id
    station = update.message.text
    
    db = Sqlite('meteo.db')
    db.del_user_river(chatid=chatid,station=station)
    db.commit_and_close()
    
    await update.message.reply_text(text="done!",reply_markup=telegram.ReplyKeyboardRemove())
    
    return -1

async def cancel(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    """Cancels and ends the conversation."""

    return ConversationHandler.END


remove_convo = ConversationHandler(entry_points=[CommandHandler("remove", remove)],
                         states= {0:[MessageHandler(filters=filters.ALL,callback=remove_done)]},
                         fallbacks=[CommandHandler("cancel",cancel)])
