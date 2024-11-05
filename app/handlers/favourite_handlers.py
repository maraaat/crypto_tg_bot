from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

import app.keyboards.keyboards as kb
from app.parser import get_coin_data_by_name, get_coin_by_id
from app.database.requests import set_user, add_favourite_coins, delete_favourite_coins, get_users_favourite, \
    invert_notifications_status
from app.apsched import start_scheduler, remove_scheduler

favourite_router = Router()


# Работа с реплай кнопками
@favourite_router.message(F.text == 'Избранное')
async def show_coin_list(message: Message):
    await message.delete()
    await message.answer(
        'Посмотреть курс нажатием на тикер. Можете нажать редактировать нажав на кнопку в конце.',
        reply_markup=await kb.get_fav_coins_kb(message.from_user.id))


# Получить список избранных монет
@favourite_router.callback_query(F.data.startswith('get-fav_'))
async def get_favourite_coin(callback: CallbackQuery):
    await callback.message.delete()
    coin_id = int(callback.data.split('_')[1])
    res = get_coin_by_id(coin_id)
    await callback.message.answer(f"Name: {res['name']}\n"
                                  f"Symbol: {res['symbol']}\n"
                                  f"Price: {round(float(res['values']['USD']['price']), 10)}")
    await callback.message.answer(
        f"Посмотреть курс нажатием на тикер. Можете нажать редактировать нажав на кнопку в конце.",
        reply_markup=await kb.get_fav_coins_kb(callback.from_user.id))


# Переход к редактированию избранного
@favourite_router.callback_query(F.data == "edit_favourite")
async def edit_favourite_list(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        'Если нажмете на тикер, то он удалится из избранного. Для выхода нажмите на кнопку в конце',
        reply_markup=await kb.edit_fav_coins_kb(callback.from_user.id))


# При нажатии на монету в избранном, она удалится (после нажатия кнопки редактировать)
@favourite_router.callback_query(F.data.startswith('edit-fav_'))
async def edit_favourite_list(callback: CallbackQuery):
    await callback.message.delete()
    await delete_favourite_coins(int(callback.data.split("_")[1]))
    await callback.message.answer(
        'Если нажмете на тикер, то он удалится из избранного. Для выхода нажмите на кнопку в конце',
        reply_markup=await kb.edit_fav_coins_kb(callback.from_user.id)
    )


# После отображения избранных монет, по кнопке "Показать все" отобразятся котировки каждой избранной монеты
@favourite_router.callback_query(F.data == "show_course_fav_coins")
async def edit_favourite_list(callback: CallbackQuery):
    await callback.message.delete()

    coins = await get_users_favourite(callback.from_user.id)
    for coin in coins:
        tmp = get_coin_by_id(int(coin.currency_id))
        await callback.message.answer(f"Name: {tmp['name']}\n"
                                      f"Symbol: {tmp['symbol']}\n"
                                      f"Price: {round(float(tmp['values']['USD']['price']), 10)}"
                                      )
    await callback.message.answer(
        'Посмотреть курс нажатием на тикер.',
        reply_markup=await kb.get_fav_coins_kb(callback.from_user.id)
    )


# Открытие меню со списком всех монет, для их добавление в избранное
@favourite_router.callback_query(F.data == "add_favourite_coins")
async def edit_favourite_list(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        'Если нажать на тикер, то добавится в избранное',
        reply_markup=await kb.get_all_coins_kb_and_exit()
    )


# После нажатия на монету, создание запроса с айди этой монеты, и последующее ее добавление в избранное
@favourite_router.callback_query(F.data.startswith('coin-add_'))
async def show_coin_data(callback: CallbackQuery):
    res = get_coin_data_by_name(callback.data.split('_')[1])
    await callback.answer(text=f"{get_coin_by_id(int(res['id']))['symbol']} добавлен в избранное")
    await add_favourite_coins(callback.from_user.id, res['id'])


# Завершить редактирование избранного
@favourite_router.callback_query(F.data == "finish_editing")
async def edit_favourite_list(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        'Посмотреть курс нажатием на тикер.',
        reply_markup=await kb.get_fav_coins_kb(callback.from_user.id)
    )
