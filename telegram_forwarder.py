import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Environment Variables থেকে কনফিগারেশন নেয়া
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SOURCE_CHAT = int(os.environ.get("SOURCE_CHAT", 0))
TARGET_CHAT = int(os.environ.get("TARGET_CHAT", 0))

# সেশন স্ট্রিং সরাসরি কোডে দেওয়া হলো
SESSION_STRING = "1BJWap1wBu30X8F9Hm1fvVu0XA9rUCLARRzUvjpWpioiym9dueziJ0koDBXFVBhejc7skVS3LqUUg6AWhi2QxDKfq_DMON2ELV0ZMsXp3EQ5dYu34zFlRJQoJA1kqaLEIDrKRQbTmnXpgYzKdZA6ommwJr8kxYPuc5IVKiSkr06RxF8KsdyLdb9mhrrbyhsxwOuUzYfAjDLXcsKT2ngVVxD77JPUHkppJ7FQ6tFS0v2B31q7E7hQWmNr33yTpi4FXs4b84fZgKWRhsnfQ11y1jVum3LGaESVoEeLL3EoW2KzszNuHRUuvw9MMmKF0oWLCSaG1EnzwttL6Owij_b9FmLFCmyH9z0="

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
