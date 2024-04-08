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
# RESPONSE_MESSAGE = "You have to join this channel first https://t.me/+dcABabRb3ioxMzM1"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

REQUIRED_CHANNEL_ID = -1002100129931  # Replace with the actual channel ID
joined_users = []  # List to store IDs of joined users
BOT_URL = "https://rplymsg-bbaa77329b52.herokuapp.com/"  # Replace with your Heroku URL



@app.on_message(filters.private & ~filters.user(EXCLUDED_USER_IDS))
def echo_handler(client, message):
    user_id = message.chat.id

    if user_id not in user_data or not user_data[user_id]:
        # User hasn't joined the required channel yet
        client.send_message(user_id, "Please join the channel first: https://t.me/+dcABabRb3ioxMzM1")
        return  # Stop sending further messages

    # User is in the channel, send the response
    client.send_message(user_id, RESPONSE_MESSAGE)

def check_channel_membership(client, user_id):
    """Checks if a user has joined the required channel"""
    try:
        member = client.get_chat_member(REQUIRED_CHANNEL_ID, user_id)
        user_data[user_id] = True  # Mark the user as joined
    except Exception as e: 
        print(f"Error checking membership for user {user_id}: {e}")
        
def keep_alive():
    """Pings the bot's URL every 10 seconds"""
    while True:
        try:
            requests.get(BOT_URL)
        except:
            pass
        time.sleep(30)

@app.on_callback_query()
def handle_callback_query(client, query):
    if query.data == "check_membership":  # Use a button or some other way for the user to trigger
        check_channel_membership(client, query.from_user.id)

if __name__ == "__main__":
    print("Bot starting...")
    # Periodically check the membership in a separate thread
    check_thread = threading.Thread(target=lambda: 
                                    while True: 
                                        for user_id in user_data: check_channel_membership(app, user_id))
    check_thread.start()
    app.run()
