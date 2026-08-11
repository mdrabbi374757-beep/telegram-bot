import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Simple Web Health Check Server (No Flask needed)
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
        
    def log_message(self, format, *args):
        return

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    server.serve_forever()

# Start background server for Render
threading.Thread(target=run_server, daemon=True).start()

# Telethon Forwarder Setup
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
