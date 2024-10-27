from datetime import datetime, timedelta

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao import BaseDAO
from app.models import dto
from app.models.db import Message


class MessageDAO(BaseDAO[Message]):
    def __init__(self, session: AsyncSession):
        super().__init__(Message, session)

    async def insert_message(self, message: dto.Message) -> dto.Message:
        kwargs = dict(
            message_id=message.message_id,
            chat_id=message.chat_id,
            sent_at=datetime.now(),
        )
        saved_message = await self.session.execute(
            insert(Message)
            .values(**kwargs)
            .returning(Message)
        )
        return saved_message.scalar_one().to_dto()

    async def get_message_ids_by_chat_id(self, chat_id: int) -> list[int]:
        time_threshold = datetime.now() - timedelta(hours=48)

        result = await self.session.execute(
            select(Message.message_id).where(Message.chat_id == chat_id, Message.sent_at >= time_threshold)
        )
        message_ids = result.scalars().all()
        return list(message_ids)