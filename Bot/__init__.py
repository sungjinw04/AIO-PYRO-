import asyncio
import time
import signal
from pyrogram import Client
from aiogram import Bot as AioBot, Dispatcher as AioDispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from .config import api_id, api_hash, bot_token
import sys

loop = asyncio.get_event_loop()

# Pyrogram Client instance
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Aiogram Bot and Dispatcher
aiobot = AioBot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = AioDispatcher(storage=storage)
router = Router()
clan = Router()
dp.include_router(router)
dp.include_router(clan)

StartTime = time.time()
BOT_ID: int = 0
BOT_USERNAME: str = ""
MENTION_BOT: str = ""

async def get_readable_time(seconds: int) -> str:
    time_string = ""
    if seconds < 0:
        raise ValueError("Input value must be non-negative")

    if seconds < 60:
        time_string = f"{round(seconds)}s"
    else:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        if days > 0:
            time_string += f"{round(days)}days, "
        if hours > 0:
            time_string += f"{round(hours)}h:"
        time_string += f"{round(minutes)}m:{round(seconds):02d}s"

    return time_string

async def init_bot():
    global BOT_NAME, BOT_USERNAME, BOT_ID, MENTION_BOT
    print("Connecting to the Telegram API...")
    try:
        await app.start()
        print("Connected")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    details = await app.get_me()
    BOT_ID = details.id
    BOT_USERNAME = details.username
    BOT_NAME = details.first_name
    MENTION_BOT = details.mention

    print(
        f"Your Bot Info:\n‣ Bot ID: {BOT_ID}\n‣ Bot Name: {BOT_NAME}\n‣ Bot Username: {BOT_USERNAME}"
    )

async def stop():
    """Stop both Pyrogram and Aiogram bots gracefully."""
    print("Stopping the bots...")
    try:
        await app.stop()  # Stop the Pyrogram client
        await aiobot.session.close()  # Close the Aiogram bot session
        await dp.shutdown()  # Shutdown the Aiogram dispatcher
        await storage.close()  # Close the storage
        await storage.wait_closed()  # Wait for the storage to close completely
        print("Bots stopped gracefully.")
    except Exception as e:
        print(f"Error during shutdown: {e}")

async def main():
    await init_bot()
    loop.create_task(dp.start_polling(aiobot))

def signal_handler(sig, frame):
    """Handle termination signals."""
    print(f"Received signal {sig}. Initiating shutdown...")
    loop.create_task(stop())  # Trigger the stop process
    loop.stop()  # Stop the event loop

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl + C
signal.signal(signal.SIGTERM, signal_handler) # Handle Ctrl + Z

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        loop.run_until_complete(stop())
        loop.close()
