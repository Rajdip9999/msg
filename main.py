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
RESPONSE_MESSAGE = "You have to join this channel first https://t.me/+dcABabRb3ioxMzM1"

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
async def echo_handler(client, message):
    """Handles incoming messages and sends the response"""
    try:
        user_status = await client.get_chat_member(
            chat_id=REQUIRED_CHANNEL_ID, user_id=message.from_user.id
        )
        if user_status.status in [
            "member",
            "creator",
            "administrator",
        ]:  # Check if they've joined
            return  # Stop messaging if the user is in the channel
    except Exception as e:
        print(f"Error checking channel membership: {e}")  # Log any errors

    client.send_message(
        message.chat.id, RESPONSE_MESSAGE
    )  # Only send if not in channel


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
