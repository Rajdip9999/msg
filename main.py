import pyrogram
from pyrogram import Client, filters
import requests  # For making the pinging requests
import threading
import time

# Replace with your actual Telegram API credentials
API_ID = 29146699  # Your API ID
API_HASH = "7625bbb67f28bd371682b737ebfe6d3a"
BOT_TOKEN = "7004730419:AAFSHpKZvF7Ax5teAZvanWk4Gc0rITFtCwE"


# IDs of users you don't want to respond to
EXCLUDED_USER_IDS = [710543063, 6444822565]  # Replace with actual user IDs

# The message you want to send
RESPONSE_MESSAGE = "You have to join this channel first @DextiNBots"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

REQUIRED_CHANNEL_ID = -1002100129931  # Replace with the actual channel ID
joined_users = []  # List to store IDs of joined users
BOT_URL = "https://rplymsg-bbaa77329b52.herokuapp.com/"  # Replace with your Heroku URL


@app.on_chat_member_updated()
def track_channel_joins(client, update):
    if (
        update.chat.id == REQUIRED_CHANNEL_ID
        and update.new_chat_member.status == "member"
    ):
        joined_users.append(update.new_chat_member.user.id)


@app.on_message(filters.private & ~filters.user(EXCLUDED_USER_IDS))
def echo_handler(client, message):
    if message.chat.id not in joined_users:
        client.send_message(message.chat.id, RESPONSE_MESSAGE)


def keep_alive():
    """Pings the bot's URL every 10 seconds"""
    while True:
        try:
            requests.get(BOT_URL)
        except:
            pass
        time.sleep(30)


@app.on_message(filters.private & ~filters.user(EXCLUDED_USER_IDS))
def echo_handler(client, message):
    global is_sending
    if is_sending:
        client.send_message(message.chat.id, RESPONSE_MESSAGE)


# Start the pinging thread
ping_thread = threading.Thread(target=keep_alive)
ping_thread.start()
if __name__ == "__main__":
    print("Bot starting...")
    app.run()
