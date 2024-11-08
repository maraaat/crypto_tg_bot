from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.parser import get_page, get_coin_by_id
from app.database.requests import get_users_favourite, get_notifications_status


# Клавиатура, с отображение всех монет с парсера
async def get_all_coins_kb():
    currencies = get_page()
    keyboard = InlineKeyboardBuilder()
    for curr in currencies:
        keyboard.add(InlineKeyboardButton(text=curr['symbol'], callback_data=f"coin_{curr['symbol']}"))

    return keyboard.adjust(4).as_markup()


# Клавиатура для добавление в избранное, т.е. есть выход из нее
async def get_all_coins_kb_and_exit():
    currencies = get_page()
    keyboard = InlineKeyboardBuilder()
    i = 0
    for curr in currencies:
        keyboard.add(InlineKeyboardButton(text=curr['symbol'], callback_data=f"coin-add_{curr['symbol']}"))
        i += 1
        if i == 99:
            break
    keyboard.add(InlineKeyboardButton(text='Выход', callback_data='finish_editing'))

    return keyboard.adjust(4).as_markup()


# Клавиатура с отображение избранных монет и функциями
async def get_fav_coins_kb(tg_id):
    coins = await get_users_favourite(tg_id)

    keyboard = InlineKeyboardBuilder()

    for coin in coins:
        keyboard.add(InlineKeyboardButton(
            text=str(get_coin_by_id(int(coin.currency_id))['symbol']),
            callback_data=f"get-fav_{coin.currency_id}")
        )
    keyboard.row(
        InlineKeyboardButton(text="Редактировать", callback_data="edit_favourite"),
        InlineKeyboardButton(text="Добавить", callback_data="add_favourite_coins"),
        InlineKeyboardButton(text="Вывести все", callback_data="show_course_fav_coins"),
    )
    notification_status = await get_notifications_status(tg_id)
    if notification_status:
        keyboard.add(InlineKeyboardButton(text="Выкл. уведомления", callback_data="disable_notifications"))
    else:
        keyboard.add(InlineKeyboardButton(text="Вкл. уведомления", callback_data="enable_notifications"))


    return keyboard.adjust(3).as_markup()


# Клавиатура с отображением избранных и возможность их удалять
async def edit_fav_coins_kb(tg_id):
    currencies = await get_users_favourite(tg_id)

    keyboard = InlineKeyboardBuilder()

    for curr in currencies:
        keyboard.add(InlineKeyboardButton(text=str(get_coin_by_id(int(curr.currency_id))['symbol']),
                                          callback_data=f"edit-fav_{curr.currency_id}"))
    keyboard.add(InlineKeyboardButton(text="Завершить", callback_data="finish_editing"))
    return keyboard.adjust(4).as_markup()


# Клавиатура с основными кнопками, которые в меню
async def main_menu_kb():
    kb = [
        [KeyboardButton(text="Избранное"), KeyboardButton(text="Общий список")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
