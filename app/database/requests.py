from app.database.models import async_session
from app.database.models import User, Currency
from sqlalchemy import select, delete, update


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(tg_id == User.tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def add_favourite_coins(tg_id, curr_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(tg_id == User.tg_id))
        curr = await session.scalar((select(Currency).where(curr_id == Currency.currency_id)))

        if not curr:
            session.add(Currency(currency_id=curr_id, user=user.id))
            await session.commit()


async def delete_favourite_coins(curr_id):
    async with async_session() as session:
        await session.execute(delete(Currency).where(Currency.currency_id == curr_id))

        await session.commit()


async def get_users_favourite(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(tg_id == User.tg_id))
        currencies = await session.scalars(select(Currency).where(user.id == Currency.user))

        return currencies.all()
