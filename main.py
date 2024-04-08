import pyrogram
from pyrogram import Client, filters
import requests
import threading
import time
import logging

# Replace with your Telegram API credentials
API_ID = 45345
API_HASH = "456456"
BOT_TOKEN = "7004730419:456"

# IDs of users you don't want to respond to
EXCLUDED_USER_IDS = [12345678, 87654321]

# The message you want to send
RESPONSE_MESSAGE = "If you want to use this bot you have to join this channel first: https://t.me/+dcABabRb3ioxMzM1"

# Heroku URL for pinger
BOT_URL = "https://rplymsg-bbaa77329b52.herokuapp.com/"

# Basic Logging (optional)
logging.basicConfig(level=logging.INFO)

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def keep_alive():
    """Pings the bot's URL every 10 seconds"""
    while True:
        try:
            requests.get(BOT_URL)
        except Exception as e:
            logging.error("Ping failed: %s", e)
        time.sleep(20)


@app.on_message(filters.private & ~filters.user(EXCLUDED_USER_IDS))
def echo_handler(client, message):
    logging.info("Message received from chat ID: %s ", message.chat.id)  # Log incoming messages
    client.send_message(message.chat.id, RESPONSE_MESSAGE)


if __name__ == "__main__":
    print("Bot starting...")
    logging.info("Bot initialized.")

    # Start the pinging thread
    ping_thread = threading.Thread(target=keep_alive)
    ping_thread.start()

    app.run()
