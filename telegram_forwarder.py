import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SOURCE_CHAT = int(os.environ.get("SOURCE_CHAT", 0))
TARGET_CHAT = int(os.environ.get("TARGET_CHAT", 0))
SESSION_STRING = os.environ.get("SESSION_STRING", "").strip()

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
