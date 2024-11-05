from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import  Message

import app.keyboards.keyboards as kb
from app.database.requests import set_user

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer(
        'Добро пожаловать. Вы можете просматривать курсы как избранных криптовалют, так и всех остальных.',
        reply_markup=await kb.main_menu_kb())
