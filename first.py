import os
import logging

from telegram import Update
from telegram.ext import Updater, Filters, CallbackContext
from telegram.ext import MessageHandler, CommandHandler, InlineQueryHandler, CallbackQueryHandler


logging.basicConfig(level=logging.DEBUG)


def message_handler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat.id, text=update.message.text)


updater = Updater('5855785269:AAH9bvPpYudd2wSAvMnBTiKakCeoB92_Z_8')
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))


if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
    updater.stop()
