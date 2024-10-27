from app.dao.holder import HolderDao
from app.models import dto


async def insert_message(message_id: int, user_id: int, dao: HolderDao):
    msg = dto.Message(message_id=message_id, chat_id=user_id)
    logged_message = await dao.message.insert_message(msg)
