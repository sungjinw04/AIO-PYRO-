from Bot import app
from pyrogram import filters

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hello from Pyrogram!")