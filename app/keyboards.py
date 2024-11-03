from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.parser import get_page, get_coin_by_id
from app.database.requests import get_users_favourite


async def get_all_coins_kb():
    currencies = get_page()
    keyboard = InlineKeyboardBuilder()
    for curr in currencies:
        keyboard.add(InlineKeyboardButton(text=curr['symbol'], callback_data=f"coin_{curr['symbol']}"))

    return keyboard.adjust(4).as_markup()


async def get_fav_coins_kb(tg_id):
    currencies = await get_users_favourite(tg_id)

    keyboard = InlineKeyboardBuilder()

    for curr in currencies:
        keyboard.add(InlineKeyboardButton(text=str(get_coin_by_id(int(curr.currency_id))), callback_data="favourite"))

    return keyboard.adjust(4).as_markup()


async def main_menu_kb():
    keyb = [
        [KeyboardButton(text="Избранное"), KeyboardButton(text="Общий список")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=keyb, resize_keyboard=True)
    return keyboard
