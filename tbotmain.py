import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask, request

# Your bot token from BotFather
BOT_TOKEN = "7568240670:AAGmfu8r63g"

# Flask app to keep bot running on Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# Telegram Bot Functions
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me a Terabox link to download.")

async def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text

    if "terabox.com" not in url:
        await update.message.reply_text("❌ This is not a valid Terabox link!")
        return

    await update.message.reply_text("🔄 Processing your request...")

    # Placeholder for downloading logic
    await update.message.reply_text("⚠️ Direct download method not working yet!")

def main():
    # Initialize bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
