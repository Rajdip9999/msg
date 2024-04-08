import pyrogram
from pyrogram import Client, filters
import requests
import threading
import time
import logging

# Replace with your Telegram API credentials
API_ID = 29146699
API_HASH = "7625bbb67f28bd371682b737ebfe6d3a"
BOT_TOKEN = "7004730419:AAFSHpKZvF7Ax5teAZvanWk4Gc0rITFtCwE"

# IDs of users you don't want to respond to
EXCLUDED_USER_IDS = [12345678, 87654321]

# The message you want to send
RESPONSE_MESSAGE = "If you want to use this bot you have to join this channel first: https://t.me/+dcABabRb3ioxMzM1"

# Required channel details
REQUIRED_CHANNEL_ID = -1002100129931

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
async def echo_handler(client, message):
    """Handles incoming messages and sends the response"""
    try:
        user_status = await client.get_chat_member(
            chat_id=REQUIRED_CHANNEL_ID, user_id=message.from_user.id
        )
        if user_status.status in ["member", "creator", "administrator"]:
            logging.info(
                f"User {message.from_user.id} is in the channel. Message not sent."
            )
            return
    except Exception as e:
        logging.error(f"Error checking channel membership: {e}")

    client.send_message(message.chat.id, RESPONSE_MESSAGE)


if __name__ == "__main__":
    print("Bot starting...")
    logging.info("Bot initialized.")

    # Start the pinging thread
    ping_thread = threading.Thread(target=keep_alive)
    ping_thread.start()

    app.run()
