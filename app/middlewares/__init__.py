from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.dao.message import MessageDAO
from app.middlewares.db_middleware import DBMiddleware
from app.middlewares.message_middleware import MessageMiddleware


async def setup_middlewares(dp: Dispatcher, pool: async_sessionmaker[AsyncSession]):
    dp.update.middleware(DBMiddleware(pool))
    async with pool() as session:
        dp.update.middleware(MessageMiddleware(MessageDAO(session)))
    # dp.message.middleware(MessageMiddleware(pool))
    # dp.inline_query.middleware(MessageMiddleware(pool))

