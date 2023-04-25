import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from modules.wrappers import Sqlite
import os
from tabulate import tabulate


async def hello(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update)
    await update.message.reply_text(reply_markup="ye",text="test")
    


async def add(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    rivers = Sqlite('meteo.db').read_unique_rivers()
    buttons = [[telegram.KeyboardButton(text=str(i[0])) ]for i in rivers]
    test = telegram.ReplyKeyboardMarkup(keyboard=buttons,one_time_keyboard=True)
    await update.message.reply_text(reply_markup=test,text="Choose the appropriate river/lake")
    
    return 0
    
async def add_station(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["river"] = update.message.text
    
    stations = Sqlite('meteo.db').read_river_stations(update.message.text)
    buttons = [[telegram.KeyboardButton(text=str(i[0])) ]for i in stations]
    kb = telegram.ReplyKeyboardMarkup(keyboard=buttons,one_time_keyboard=True)
    
    
    await update.message.reply_text(reply_markup=kb,text="Choose the obs. station")
    
    return 1


async def add_level(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["station"] = update.message.text
    
    await update.message.reply_text(text="enter the threshold, in m")
    
    return 2



async def add_done(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    level = update.message.text
    station = context.user_data["station"]
    chatid = update.message.chat_id
    
    db = Sqlite('meteo.db')
    db.new_user_river(chatid=chatid,threshold=level,station=station)
    db.commit_and_close()
    
    await update.message.reply_text(text="done!",reply_markup=telegram.ReplyKeyboardRemove())
    
    return -1


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
async def mystations(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db = Sqlite('meteo.db')
    chatid = int(update.message.chat_id)
    user_rivers = db.read_user_rivers(chatid=chatid)
    
    header = ("River/Lake", "Threshold Lvl.")
    print(user_rivers)
    table = tabulate(user_rivers,headers=header)
    table = "``` Current watchlist:\n\n" + table + "```"
    
    await update.message.reply_text(text=table,parse_mode="MarkdownV2")
    



async def cancel(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    """Cancels and ends the conversation."""
    print(context.user_data["t"])

    return ConversationHandler.END


mystations = CommandHandler("mystations",mystations)
start = CommandHandler("start",hello)

app = ApplicationBuilder().token(os.environ["TGBOT_TOKEN"]).build()
add_convo = ConversationHandler(entry_points=[CommandHandler("add", add)],
                         states= {0:[MessageHandler(filters=filters.ALL,callback=add_station)],
                                  1:[MessageHandler(filters=filters.ALL,callback=add_level)],
                                  2:[MessageHandler(filters=filters.Regex(r"\d+"),callback=add_done)]},
                         fallbacks=[CommandHandler("cancel",cancel)])

remove_convo = ConversationHandler(entry_points=[CommandHandler("remove", remove)],
                         states= {0:[MessageHandler(filters=filters.ALL,callback=remove_done)]},
                         fallbacks=[CommandHandler("cancel",cancel)])


app.add_handler(add_convo)
app.add_handler(remove_convo)
app.add_handler(mystations)
app.run_polling()
