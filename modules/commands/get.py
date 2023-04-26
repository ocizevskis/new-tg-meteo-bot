import telegram
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from modules.wrappers import Sqlite
from modules.commands import cancel
import requests
import os

async def get_river(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    rivers = Sqlite('meteo.db').read_unique_rivers()
    buttons = [[i[0]] for i in rivers]
    context.user_data["allowed_choices"] = [i[0] for i in buttons]
    
    test = telegram.ReplyKeyboardMarkup(keyboard=buttons,one_time_keyboard=True)
    
    await update.message.reply_text(reply_markup=test,text="Choose the appropriate river/lake")
    
    return 0
    
async def get_station(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    if update.message.text not in context.user_data["allowed_choices"]:
        await update.message.reply_text(text="you done goofed. Try again.")
        
        return 0
    
    context.user_data["river"] = update.message.text
    
    stations = Sqlite('meteo.db').read_river_stations(update.message.text)
    buttons = [[i[0] ]for i in stations]
    context.user_data["allowed_choices"] = [i[0] for i in buttons]
    kb = telegram.ReplyKeyboardMarkup(keyboard=buttons,one_time_keyboard=True)
    
    
    await update.message.reply_text(reply_markup=kb,text="Choose the obs. station")
    
    return 1

async def get_done(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    station = update.message.text
    station = station[0].upper() + station[1:]
    
    if station not in context.user_data["allowed_choices"]:
        await update.message.reply_text(text=f"{station} is not a valid station name. Try again, or use the custom keyboard.")
        
        return 1
    
    db = Sqlite('meteo.db')
    data = db.read(f"select * from data where station = '{station}'")[0]
    db.commit_and_close()
    
    
    text = f"""Pašreizējais ūdens līmenis stacijā '{data["station"]}': {data["level"]}m. Dati pēdējoreiz atjaunināti {data["date"]}"""
    
    image = requests.get(f'https://hidro.meteo.lv/hymer/images/{data["plot_url"]}').content

    
    await update.message.reply_text(text=text,reply_markup=telegram.ReplyKeyboardRemove())
    await update.message.reply_photo(photo=image)
    
    return -1

convo = ConversationHandler(entry_points=[CommandHandler("get", get_river)],
                         states= {0:[MessageHandler(filters=filters.ALL,callback=get_station)],
                                  1:[MessageHandler(filters=filters.ALL,callback=get_done)]},
                         fallbacks=[CommandHandler("cancel",cancel.cancel)])

