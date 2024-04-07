import pyrogram
from pyrogram import Client, filters

# Replace with your actual Telegram API credentials
API_ID = 29146699  # Your API ID
API_HASH = "7625bbb67f28bd371682b737ebfe6d3a"
BOT_TOKEN = "6405792409:AAEpzhXGcJ89O4SGoHiFpW3NMLf85jwLIZ4"

# IDs of users you don't want to respond to
EXCLUDED_USER_IDS = [710543063, 6444822565]  # Replace with actual user IDs

# The message you want to send
RESPONSE_MESSAGE = "Use this bot this bot is down:\n@Terabox_Video_Robot\n@Terabox_Video_Robot\n@Terabox_Video_Robot\n@Terabox_Video_Robot"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.private & ~filters.user(EXCLUDED_USER_IDS))
def echo_handler(client, message):
    """Handles incoming messages and sends the response"""
    client.send_message(message.chat.id, RESPONSE_MESSAGE)


if __name__ == "__main__":
    print("Bot starting...")
    app.run()
