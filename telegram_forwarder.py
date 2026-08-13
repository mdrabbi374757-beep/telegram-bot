import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Render Web Port Health Check
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"OK")
        
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        return

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# Environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SOURCE_CHAT = int(os.environ.get("SOURCE_CHAT", 0))
TARGET_CHAT = int(os.environ.get("TARGET_CHAT", 0))

# Clean raw session string
SESSION_STRING = os.environ.get("SESSION_STRING", "").strip().strip("'").strip('"')

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def handler(event):
    try:
        # ১. শুধুমাত্র মেসেজের লেখা (Text) বের করা
        text = event.raw_text or event.text
        
        # যদি কোনো টেক্সট না থাকে, তবে স্কিপ করবে
        if not text:
            return

        # ২. TBM নামটি পরিবর্তন করে VIP AUTO বসানো
        text = text.replace("TBM PRE-ENTRY ALERT", "VIP AUTO PRE-ENTRY ALERT")
        text = text.replace("TBM PREMIUM SIGNAL", "VIP AUTO PREMIUM SIGNAL")
        text = text.replace("TBM", "VIP AUTO")

        # ৩. কোনো ছবি ছাড়া শুধুমাত্র লেখা ফরওয়ার্ড করা
        await client.send_message(TARGET_CHAT, text)
        print("Text signal forwarded successfully!")
    except Exception as e:
        print(f"Error forwarding message: {e}")

async def main():
    print("Starting Telegram forwarding service...")
    await client.start()
    print("Telegram session authenticated; waiting for new messages")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
