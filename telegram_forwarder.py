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

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SOURCE_CHAT = int(os.environ.get("SOURCE_CHAT", 0))
TARGET_CHAT = int(os.environ.get("TARGET_CHAT", 0))
SESSION_STRING = os.environ.get("SESSION_STRING", "").strip().strip("'").strip('"')

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def handler(event):
    # শুধু টেক্সট মেসেজ হলে প্রসেস করবে
    if event.raw_text:
        text = event.raw_text
        
        # এখানে TBM মুছে আপনার চ্যানেলের নাম বসানো হচ্ছে
        new_text = text.replace("TBM", "VIP AUTO AI")
        
        # ছবি ছাড়া শুধু টেক্সট পাঠানোর কমান্ড
        await client.send_message(TARGET_CHAT, new_text)
        print("Signal forwarded with updated name!")

async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
