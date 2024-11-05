import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.parser import get_page
from app.handlers.notifications_handlers import notif_router
from app.handlers.show_handlers import show_router
from app.handlers.favourite_handlers import favourite_router

from app.database.models import async_main
from app.apsched import load_users_with_notifications

from app.apsched import scheduler


async def main():
    await async_main()
    get_page()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(notif_router, show_router, favourite_router)

    scheduler.start()
    await load_users_with_notifications(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
