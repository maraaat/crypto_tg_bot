from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

import app.keyboards.keyboards as kb
from app.parser import get_coin_data_by_name, get_coin_by_id
from app.database.requests import set_user, add_favourite_coins, delete_favourite_coins, get_users_favourite, invert_notifications_status
from app.apsched import start_scheduler, remove_scheduler

show_router = Router()


@show_router.message(F.text == 'Общий список')
async def show_coin_list(message: Message):
    await message.delete()
    await message.answer('Если нажать на тикер, то получите текущий курс монеты',
                         reply_markup=await kb.get_all_coins_kb())



@show_router.callback_query(F.data.startswith('coin_'))
async def show_coin_data(callback: CallbackQuery):
    res = get_coin_data_by_name(callback.data.split('_')[1])
    # await add_favourite_coins(callback.from_user.id, res['id'])
    await callback.message.answer(f"Name: {res['name']}\n"
                                  f"Symbol: {res['symbol']}\n"
                                  f"Price: {round(float(res['values']['USD']['price']), 10)}",
                                  )
