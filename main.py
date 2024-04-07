import pyrogram
from pyrogram import Client, filters
import requests  # For making the pinging requests
import threading
import time

# Replace with your actual Telegram API credentials
API_ID = 28015381  # Your API ID
API_HASH = "d1be9454b29326ed41b0acdef11d202c"
BOT_TOKEN = "7088928556:AAFulnC-duhQj2mMgyQSt0vob-KKBz3Gk-0"

CONTROL_BOT_TOKEN = (
    "7004730419:AAFSHpKZvF7Ax5teAZvanWk4Gc0rITFtCwE"  # Token of your control bot
)
CONTROL_BOT_ID = 29146699
CONTROL_BOT_HASH = "7625bbb67f28bd371682b737ebfe6d3a"


# IDs of users you don't want to respond to
EXCLUDED_USER_IDS = [710543063, 6444822565]  # Replace with actual user IDs

# The message you want to send
RESPONSE_MESSAGE = "Use this bot this bot is down:\n@TeraboxVideoDownloadRobot\n@TeraboxVideoDownloadRobot"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
control_bot = Client(
    "control_bot",
    api_id=CONTROL_BOT_ID,
    api_hash=CONTROL_BOT_HASH,
    bot_token=CONTROL_BOT_TOKEN,
)

BOT_URL = "https://rplymsg-bbaa77329b52.herokuapp.com/"  # Replace with your Heroku URL

is_sending = False  # Flag to track sending status


@app.on_message(filters.private & ~filters.user(EXCLUDED_USER_IDS))
def echo_handler(client, message):
    """Handles incoming messages and sends the response"""
    client.send_message(message.chat.id, RESPONSE_MESSAGE)


def keep_alive():
    """Pings the bot's URL every 10 seconds"""
    while True:
        try:
            requests.get(BOT_URL)
        except:
            pass
        time.sleep(20)


@app.on_message(filters.private & ~filters.user(EXCLUDED_USER_IDS))
def echo_handler(client, message):
    global is_sending
    if is_sending:
        client.send_message(message.chat.id, RESPONSE_MESSAGE)


@control_bot.on_message(filters.command(["start", "stop"]))
def control_handler(client, message):
    global is_sending
    if message.command[0] == "start":
        is_sending = True
        client.send_message(message.chat.id, "Message sending started.")
    elif message.command[0] == "stop":
        is_sending = False
        client.send_message(message.chat.id, "Message sending stopped.")


# ... (Start both bots) ...
ping_thread = threading.Thread(target=keep_alive)
ping_thread.start()


# Start the pinging thread
ping_thread = threading.Thread(target=keep_alive)
ping_thread.start()
if __name__ == "__main__":
    print("Bot starting...")
    app.run()
    control_bot.run()
