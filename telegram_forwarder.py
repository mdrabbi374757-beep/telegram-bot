import os
import asyncio
from threading import Thread
from flask import Flask
from telethon import TelegramClient
from telethon.sessions import StringSession

# --- Render Port Error সমাধানের জন্য Flask Server ---
app = Flask('')

@app.route('/')
def home():
    return "Telegram Forwarder Bot is Running!"

def run_flask():
    # Render নিজে থেকে PORT এনভাইরনমেন্ট ভ্যারিয়েবল সেট করে নেয়, না থাকলে ১০০০০ পোর্ট ব্যবহার করবে
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    server_thread = Thread(target=run_flask)
    server_thread.daemon = True
    server_thread.start()

# --- আপনার টেলিগ্রাম বটের মূল কোড ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def main():
    print("Bot starting...")
    await client.start()
    print("Bot is logged in successfully!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    # ১. প্রথমে ব্যাকগ্রাউন্ডে পোর্টের জন্য Web Server চালু হবে
    keep_alive()
    
    # ২. এরপর টেলিগ্রাম বট রান হবে
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
