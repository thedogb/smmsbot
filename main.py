import telegram
from flask import Flask
from flask import request
from queue import Queue
from telegram.ext import Filters, MessageHandler, CallbackQueryHandler
from telegram.ext import Dispatcher
from tools import upload_handler, callback_handler, error_handler, upload_sticker_handler
from credentials import TOKEN, APP_URL


from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

app = Flask(__name__)

global bot
bot = telegram.Bot(token=TOKEN)
dp = Dispatcher(bot, Queue(), workers=10)
dp.add_handler(MessageHandler(Filters.document, upload_handler))
dp.add_handler(MessageHandler(Filters.photo, upload_handler))
dp.add_handler(MessageHandler(Filters.sticker, upload_sticker_handler))
dp.add_handler(CallbackQueryHandler(callback_handler))
dp.add_error_handler(error_handler)

@app.route('/HOOK', methods=['POST', 'GET'])
def webhook_handler():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dp.process_update(update)
    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook(APP_URL + '/HOOK')
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


if __name__ == '__main__':
    app.run()
