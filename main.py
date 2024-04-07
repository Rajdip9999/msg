import pyrogram
from pyrogram import Client, filters
import requests  # For making the pinging requests
import threading
import time

# Replace with your actual Telegram API credentials
API_ID = 28015381  # Your API ID
API_HASH = "d1be9454b29326ed41b0acdef11d202c"
BOT_TOKEN = "7088928556:AAFulnC-duhQj2mMgyQSt0vob-KKBz3Gk-0"

# IDs of users you don't want to respond to
EXCLUDED_USER_IDS = [710543063, 6444822565]  # Replace with actual user IDs

# The message you want to send
RESPONSE_MESSAGE = "Use this bot this bot is down:\n@Terabox_Video_Robot\n@Terabox_Video_Robot\n@Terabox_Video_Robot\n@Terabox_Video_Robot"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.private & ~filters.user(EXCLUDED_USER_IDS))
def echo_handler(client, message):
    """Handles incoming messages and sends the response"""
    client.send_message(message.chat.id, RESPONSE_MESSAGE)


BOT_URL = "https://rplymsg-bbaa77329b52.herokuapp.com/"  # Replace with your Heroku URL


def keep_alive():
    """Pings the bot's URL every 10 seconds"""
    while True:
        try:
            requests.get(BOT_URL)
            print("Ping successful")
        except:
            print("Ping failed")
        time.sleep(10)


# Start the pinging thread
ping_thread = threading.Thread(target=keep_alive)
ping_thread.start()
if __name__ == "__main__":
    print("Bot starting...")
    app.run()
