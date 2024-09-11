import asyncio
import importlib
import os
import signal

from Bot.handlers import MODULES_PATH
from rich.console import Console
from pyrogram import idle
from Bot import main as bot_main, stop as bot_stop  # Import the main and stop functions from bot/__init__.py

loop = asyncio.get_event_loop()
IMPORTED = {}

LOG = Console()

async def shutdown():
    """Shut down bots gracefully."""
    LOG.print("[bold red]Stopping bots...")
    await bot_stop()  # Call the stop function from bot/__init__.py to gracefully shut down bots
    loop.stop()

def signal_handler(sig, frame):
    """Handle termination signals."""
    LOG.print(f"[bold red]Received signal {sig}. Shutting down...")
    loop.create_task(shutdown())

async def main():
    LOG.print(f"[bold yellow]Loading {len(MODULES_PATH)} Modules")
    for module in MODULES_PATH:
        mod = module.replace(os.getcwd(),"")[1:].replace('/','.').replace(".py",'')
        LOG.print(f"[bold cyan]{mod.split('.')[-1]}")
        
        importlib.import_module(mod)

    print("✨ Bot started")
    
    await bot_main()  # Start the bots (both pyrogram and aiogram)
    await idle()  # Keep running until manually stopped

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl + C
    signal.signal(signal.SIGTERM, signal_handler) # Handle Ctrl + Z

    loop.run_until_complete(main())
