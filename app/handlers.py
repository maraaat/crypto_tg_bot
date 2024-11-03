from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

import app.keyboards as kb
from app.parser import get_coin_data_by_name
from app.database.requests import set_user, add_favourite_coins

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer('Welcome', reply_markup=await kb.main_menu_kb())


@router.message(F.text == 'Общий список')
async def show_coin_list(message: Message):
    await message.answer('Welcome', reply_markup=await kb.get_all_coins_kb())


@router.message(F.text == 'Избранное')
async def show_coin_list(message: Message):
    await message.answer('Welcome', reply_markup=await kb.get_fav_coins_kb(message.from_user.id))


@router.callback_query(F.data.startswith('coin_'))
async def show_coin_data(callback: CallbackQuery):
    res = get_coin_data_by_name(callback.data.split('_')[1])
    await add_favourite_coins(callback.from_user.id, res['id'])
    print(res)
    await callback.message.answer(f"Name: {res['name']}\n"
                                  f"Symbol: {res['symbol']}\n"
                                  f"Price: {round(float(res['values']['USD']['price']), 10)}")
