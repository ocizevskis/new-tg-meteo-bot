from telegram.ext import ApplicationBuilder
import os
from modules.commands import add, get, remove, mystations, start


app = ApplicationBuilder().token(os.environ["TGBOT_TOKEN"]).build()

app.add_handler(start.command)
app.add_handler(add.convo)
app.add_handler(remove.remove_convo)
app.add_handler(get.convo)
app.add_handler(mystations.command)
app.run_polling(timeout=60)
