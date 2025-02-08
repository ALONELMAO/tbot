import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask
import threading

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Store bot token in Render environment variables

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

async def main():
    # Initialize bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    await application.run_polling()

if __name__ == "__main__":
    # Run Telegram bot in a separate thread
    bot_thread = threading.Thread(target=lambda: asyncio.run(main()))
    bot_thread.start()

    # Run Flask app for Render Web Service
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
