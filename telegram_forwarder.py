import os
import re
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SOURCE_CHAT = int(os.environ.get("SOURCE_CHAT", 0))
TARGET_CHAT = int(os.environ.get("TARGET_CHAT", 0))

# Get raw session string
raw_session = os.environ.get("SESSION_STRING", "").strip()

if raw_session.startswith("1"):
    version = "1"
    body = raw_session[1:]
else:
    version = ""
    body = raw_session

# Clean string: Keep only valid Base64 characters
body = re.sub(r'[^A-Za-z0-9\-_=]', '', body)

# Fix Base64 padding error if 1 extra character was pasted
if len(body) % 4 == 1:
    body = body[:-1]

SESSION_STRING = version + body

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
