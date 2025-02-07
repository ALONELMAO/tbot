import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from flask import Flask

# Your bot token from BotFather
BOT_TOKEN = "7568240670:AAG0LHFpgc9p20LaDZfcb58w3AYmFu8r63g"

# Flask app to keep bot running on Render
app = Flask(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a Terabox link to download.")

def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text

    if "terabox.com" not in url:
        update.message.reply_text("❌ This is not a valid Terabox link!")
        return

    update.message.reply_text("🔄 Processing your request...")

    # Placeholder for downloading logic
    update.message.reply_text("⚠️ Direct download method not working yet!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
