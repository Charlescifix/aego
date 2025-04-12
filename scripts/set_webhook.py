# scripts/set_webhook.py
import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

async def main():
    bot = Bot(token=API_KEY)
    success = await bot.set_webhook(url=WEBHOOK_URL)

    if success:
        print(f"✅ Webhook successfully set to: {WEBHOOK_URL}")
    else:
        print("❌ Failed to set webhook.")

if __name__ == "__main__":
    asyncio.run(main())
