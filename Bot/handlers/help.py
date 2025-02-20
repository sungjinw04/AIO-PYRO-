from Bot import router
from aiogram.types import Message
from aiogram import F
from aiogram.filters import Command

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Help from Aiogram!")