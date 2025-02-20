import asyncio
import time
from pyrogram import Client
from aiogram import Bot as AioBot, Dispatcher as AioDispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from .config import api_id, api_hash, bot_token
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from rich.console import Console
from rich.logging import RichHandler

LOG_FILE = "log.txt"

open(LOG_FILE, 'w').close()


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - Cricket - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RichHandler(console=Console(), rich_tracebacks=True), 
        logging.FileHandler(LOG_FILE), 
    ]
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiogram").setLevel(logging.ERROR)
logger = logging.getLogger()


loop = asyncio.get_event_loop()
app = Client("cricketbot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
scheduler = AsyncIOScheduler()

aiobot = AioBot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = AioDispatcher(storage=storage)
router = Router()
dp.include_router(router)

DOWNLOAD_DIR = "downloads"

StartTime = time.time()
BOT_ID: int = 0
BOT_USERNAME: str = ""
MENTION_BOT: str = ""


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


async def main():
    await init_bot()
    loop.create_task(dp.start_polling(aiobot))