import os
import re
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

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SOURCE_CHAT = int(os.environ.get("SOURCE_CHAT", 0))
TARGET_CHAT = int(os.environ.get("TARGET_CHAT", 0))
SESSION_STRING = os.environ.get("SESSION_STRING", "").strip().strip("'").strip('"')

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def handler(event):
    try:
        # মেসেজের ক্যাপশন বা টেক্সট নেওয়া
        text = event.text or event.raw_text or ""
        
        # কোনো লেখা না থাকলে স্কিপ করবে
        if not text.strip():
            return

        # যেকোনো ধরনের TBM দেখলেই তা VIP AUTO AI দিয়ে বদলে দেবে
        new_text = re.sub(r'TBM', 'VIP AUTO AI', text, flags=re.IGNORECASE)

        # ছবি ছাড়া শুধু এডিট করা টেক্সট ফরওয়ার্ড করা
        await client.send_message(TARGET_CHAT, new_text)
        print("Signal text successfully updated and forwarded!")
    except Exception as e:
        print(f"Error forwarding message: {e}")

async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
