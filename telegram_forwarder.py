import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession


# Render Web Port Health Check
class HealthCheck(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"OK")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        return


def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheck)
    server.serve_forever()


threading.Thread(target=run_server, daemon=True).start()

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SOURCE_CHAT = int(os.environ.get("SOURCE_CHAT", 0))
TARGET_CHAT = int(os.environ.get("TARGET_CHAT", 0))
SESSION_STRING = os.environ.get("SESSION_STRING", "").strip().strip('"')

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def handler(event):
    if event.raw_text:
        text = event.raw_text

        # TBM এবং VIP AI স্টাইলের লেখাকে 𝐇𝐍𝐑 𝐑𝐀𝐁𝐁𝐈 𝐀𝐈 𝐁𝐎𝐓 দিয়ে রিপ্লেস করা
        new_text = text.replace("TBM ADVANCE PRO", "𝐇𝐍𝐑 𝐑𝐀𝐁𝐁𝐈 𝐀𝐈 𝐁𝐎𝐓")
        new_text = new_text.replace("TBM", "𝐇𝐍𝐑 𝐑𝐀𝐁𝐁𝐈 𝐀𝐈 𝐁𝐎𝐓")
        new_text = new_text.replace("VIP AI ADVANCE PRO", "𝐇𝐍𝐑 𝐑𝐀𝐁𝐁𝐈 𝐀𝐈 𝐁𝐎𝐓")
        new_text = new_text.replace("VIP AI", "𝐇𝐍𝐑 𝐑𝐀𝐁𝐁𝐈 𝐀𝐈 𝐁𝐎𝐓")

        # ফরওয়ার্ড করে টার্গেট চ্যানেলে পাঠানো
        await client.send_message(TARGET_CHAT, new_text)
        print("Signal text updated with 𝐇𝐍𝐑 𝐑𝐀𝐁𝐁𝐈 𝐀𝐈 𝐁𝐎𝐓 and forwarded!")


async def main():
    await client.start()
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
