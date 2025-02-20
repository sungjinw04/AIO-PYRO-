import asyncio
import importlib
import os
from pyrogram import idle
from Bot.handlers import MODULES_PATH
from Bot import main as bot_main, scheduler
from Bot import logger


loop = asyncio.get_event_loop()
IMPORTED = {}



async def main():
    logger.info(f"Loading {len(MODULES_PATH)} Modules")

    logger.info("Initializing database...")

    scheduler.start()

    # Load modules
    for module in MODULES_PATH:
        mod = module.replace(os.getcwd(), "")[1:].replace('/', '.').replace(".py", '')
        logger.info(f"Loading module: {mod.split('.')[-1]}")

        importlib.import_module(mod)

    logger.info("✨ Bot started")

    await bot_main()  
    await idle()  

if __name__ == "__main__":

    loop.run_until_complete(main())