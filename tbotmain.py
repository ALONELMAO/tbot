import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import tempfile
import shutil

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Store bot token in Render environment variables
TERABOX_EMAIL = os.getenv("TERABOX_EMAIL")  # Store Terabox email in environment variables
TERABOX_PASSWORD = os.getenv("TERABOX_PASSWORD")  # Store Terabox password in environment variables

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# Function to check file size before downloading (early check)
def check_file_size(url: str) -> float:
    # For demonstration purposes, assume a method to fetch file size
    # Ideally, this would use an API or scraping logic from Terabox to get the file size.
    # Returning a placeholder file size in GB
    # Example: returning 2.5GB which will trigger the 2GB size check.
    # Implement Terabox scraping logic to check file size here.
    
    # Placeholder file size
    file_size_gb = 2.5  # This is a placeholder, replace with actual scraping or API call
    
    return file_size_gb

# Function to download file from Terabox
def download_from_terabox(url: str) -> str:
    # Set up the browser driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # Log in to Terabox
    try:
        # Find and input login email
        email_field = driver.find_element(By.XPATH, '//input[@name="email"]')
        email_field.send_keys(TERABOX_EMAIL)

        # Find and input password
        password_field = driver.find_element(By.XPATH, '//input[@name="password"]')
        password_field.send_keys(TERABOX_PASSWORD)
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for login to complete
    except Exception as e:
        print(f"Error during login: {e}")
        return None

    # Find and click the download button (adjust based on the page structure)
    try:
        download_button = driver.find_element(By.XPATH, 'xpath_to_download_button')
        download_button.click()
        time.sleep(5)  # Wait for download to finish
    except Exception as e:
        print(f"Error during download: {e}")
        return None

    # Get the downloaded file path (modify this based on your browser's download settings)
    download_path = tempfile.mktemp(suffix='.mp4')  # Modify file type and path as per your need
    shutil.move('downloaded_file_path', download_path)  # Move to desired location
    
    driver.quit()
    return download_path

# Telegram Bot Functions
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me a Terabox link to download.")

async def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text

    if "terabox.com" not in url:
        await update.message.reply_text("❌ This is not a valid Terabox link!")
        return

    await update.message.reply_text("🔄 Processing your request...")

    # Early file size check before downloading
    file_size = check_file_size(url)
    
    if file_size > 2:
        await update.message.reply_text(f"⚠️ The file size is {file_size} GB, which exceeds Telegram's upload limit (2GB).")
        return

    # Download file using Selenium
    file_path = download_from_terabox(url)
    
    if file_path:
        await update.message.reply_text("✅ File downloaded, sending to you...")
        with open(file_path, 'rb') as file:
            await update.message.reply_document(file)
        
        os.remove(file_path)  # Clean up the downloaded file after sending
    else:
        await update.message.reply_text("⚠️ Download failed!")

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
    import threading
    import asyncio
    bot_thread = threading.Thread(target=lambda: asyncio.run(main()))
    bot_thread.start()

    # Run Flask app for Render Web Service
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
