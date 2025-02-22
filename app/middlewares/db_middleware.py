from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Update, Message
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.dao.holder import HolderDao


class DBMiddleware(BaseMiddleware):
    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        super().__init__()
        self.pool = pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        async with self.pool() as session:
            holder_dao = HolderDao(session)
            data["dao"] = holder_dao
            result = await handler(event, data)
            return result
