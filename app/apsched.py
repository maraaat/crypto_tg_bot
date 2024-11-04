import asyncio

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database.models import async_session, User
from sqlalchemy import select

from app.database.requests import get_users_favourite
from app.parser import get_coin_by_id


async def send_favourites_by_time(bot: Bot, user_id):
    try:
        coins = await get_users_favourite(user_id)
        for coin in coins:
            tmp = get_coin_by_id(int(coin.currency_id))
            await bot.send_message(user_id,
                                   f"Name: {tmp['name']}\n"
                                   f"Symbol: {tmp['symbol']}\n"
                                   f"Price: {round(float(tmp['values']['USD']['price']), 10)}"
                                   )
        #
        # await bot.send_message(user_id, "Это сообщение по расписанию!")
    except Exception as e:
        print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


scheduler = AsyncIOScheduler()


def start_scheduler(bot: Bot, user_id):
    job_id = f"notifications_{user_id}"

    if not scheduler.get_job(job_id):
        # scheduler.add_job(send_favourites_by_time(bot))
        scheduler.add_job(send_favourites_by_time, 'interval', minutes=60, args=[bot, user_id], id=job_id)


def remove_scheduler(user_id):
    job_id = f"notifications_{user_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)


async def load_users_with_notifications(bot: Bot):
    async with async_session() as session:
        users = await session.scalars(select(User).where(User.notifications == True))
        users = users.all()

        for user in users:
            start_scheduler(bot, user.tg_id)


