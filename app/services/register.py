from aiogram_dialog import DialogManager

from app.dao.holder import HolderDao
from app.models import dto


async def upsert_user(dialog_manager: DialogManager, zodiac_name, dao: HolderDao):
    user_dto = dto.User(
        tg_id=dialog_manager.event.from_user.id,
        zodiac_sign=zodiac_name,
        first_name=dialog_manager.event.from_user.first_name
    )
    await dao.user.upsert_user(user_dto)
