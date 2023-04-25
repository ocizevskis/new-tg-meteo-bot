import telegram
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from modules.wrappers import Sqlite
from modules.commands import get

async def add_level(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    station = update.message.text
    station = station[0].upper() + station[1:]
    
    if station not in context.user_data["allowed_choices"]:
        await update.message.reply_text(text=f"{station} is not a valid station name. Try again, or use the custom keyboard.")
        
        return 1
    
    context.user_data["station"] = update.message.text
    
    await update.message.reply_text(text="enter the threshold, in m")
    
    return 2

async def add_done(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    level = float(update.message.text)
    station = context.user_data["station"]
    chatid = update.message.chat_id
    
    try:
        db = Sqlite('meteo.db')
        db.new_user_river(chatid=chatid,threshold=level,station=station)
        db.commit_and_close()
        
        await update.message.reply_text(text="done!",reply_markup=telegram.ReplyKeyboardRemove())
    except:
        await update.message.reply_text(text="station already added. delete the old entry and try again.")
        
    return -1

async def cancel(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    """Cancels and ends the conversation."""

    return ConversationHandler.END


convo = ConversationHandler(entry_points=[CommandHandler("add", get.get_river)],
                         states= {0:[MessageHandler(filters=filters.ALL,callback=get.get_station)],
                                  1:[MessageHandler(filters=filters.ALL,callback=add_level)],
                                  2:[MessageHandler(filters=filters.Regex(r"\d+"),callback=add_done)]},
                         fallbacks=[CommandHandler("cancel",cancel)])