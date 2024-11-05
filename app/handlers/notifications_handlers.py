from aiogram import F, Router
from aiogram.types import CallbackQuery

import app.keyboards.keyboards as kb

from app.database.requests import invert_notifications_status
from app.apsched import start_scheduler, remove_scheduler

notif_router = Router()


@notif_router.callback_query(F.data == "enable_notifications")
async def make_enable_notifications(callback: CallbackQuery):
    await callback.message.delete()

    await invert_notifications_status(callback.from_user.id)
    start_scheduler(callback.message.bot, callback.from_user.id)

    await callback.answer("Уведомления включены!")

    await callback.message.answer(
        'Посмотреть курс нажатием на тикер.',
        reply_markup=await kb.get_fav_coins_kb(callback.from_user.id)
    )


@notif_router.callback_query(F.data == "disable_notifications")
async def make_enable_notifications(callback: CallbackQuery):
    await callback.message.delete()

    await invert_notifications_status(callback.from_user.id)
    remove_scheduler(callback.from_user.id)
    await callback.answer("Уведомления выключены!")
    await callback.message.answer(
        'Посмотреть курс нажатием на тикер.',
        reply_markup=await kb.get_fav_coins_kb(callback.from_user.id)
    )
