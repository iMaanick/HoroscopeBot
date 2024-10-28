from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, Message

from app.dao.message import MessageDAO
from app.models import dto


class MessageMiddleware(BaseMiddleware):
    def __init__(self, message: MessageDAO):
        super().__init__()
        self.message = message

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: dict[str, Any]
    ) -> Any:
        if isinstance(event.message, Message) and event.message.edit_date is None:
            msg = dto.Message(event.message.message_id, event.message.from_user.id)
            await self.message.insert_message(msg)
            await self.message.commit()
        result = await handler(event, data)
        return result
