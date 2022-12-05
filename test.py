
import logging
import json
from threading import Timer
from telegram import Update
from telegram.ext import Updater, Filters, CallbackContext,CommandHandler,MessageHandler, InlineQueryHandler, CallbackQueryHandler,ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton 



with open("data.json", 'r', encoding="utf-8") as f:
    data = json.load(f)
token=data['token']
description = data['description']
advertiseText = data['advertiseText']

logging.basicConfig(level=logging.DEBUG)
updater = Updater(token)



NEW_ACCOUNT= range(1)
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,text='start')
    return NEW_ACCOUNT
def first_handler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,text='def first_handler')
    return NEW_ACCOUNT
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('asd', start)],
    states={
        NEW_ACCOUNT: [MessageHandler(filters=Filters.text & (~ Filters.command), callback=first_handler)],
    },fallbacks=[CommandHandler('cancel', cancel)],)

def main():
    #updater.dispatcher.add_handler(MessageHandler(filters=Filters.text & (~ Filters.command), callback=message_handler))
    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
    updater.stop()

if __name__ == "__main__":
    main()
