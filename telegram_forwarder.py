import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SOURCE_CHAT = int(os.environ.get("SOURCE_CHAT", 0))
TARGET_CHAT = int(os.environ.get("TARGET_CHAT", 0))

# Get raw session string
raw_session = os.environ.get("SESSION_STRING", "").strip().replace("\n", "").replace("\r", "").replace(" ", "")

if raw_session:
    # Telethon StringSession starts with '1' as version prefix
    if raw_session.startswith("1"):
        version = raw_session[0]
        body = raw_session[1:]
    else:
        version = ""
        body = raw_session

    # If mobile paste added 1 extra character to body, trim it
    if len(body) % 4 == 1:
        body = body[:-1]

    # Auto-add missing '=' padding to body if needed
    missing_padding = len(body) % 4
    if missing_padding:
        body += "=" * (4 - missing_padding)

    SESSION_STRING = version + body
else:
    SESSION_STRING = ""

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def handler(event):
    try:
        await client.send_message(TARGET_CHAT, event.message)
        print("Forwarded a new message from the source chat")
    except Exception as e:
        print(f"Error forwarding message: {e}")

async def main():
    print("Starting Telegram forwarding service...")
    await client.start()
    print("Telegram session authenticated; waiting for new messages")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
