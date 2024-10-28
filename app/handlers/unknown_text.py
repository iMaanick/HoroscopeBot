from aiogram import Dispatcher, Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.dao.holder import HolderDao
from app.dialogs.utils import zodiac_signs
from app.services.message import insert_message


async def unknown_text(message: Message, dialog_manager: DialogManager) -> None:
    dao: HolderDao = dialog_manager.middleware_data["dao"]

    bot_msg = await message.answer("Извините, я не понял")

    await insert_message(bot_msg.message_id, message.from_user.id, dao)

    await dao.commit()


def setup_unknown_text(dp: Dispatcher) -> None:
    router = Router(name=__name__)
    router.message.register(unknown_text, F.text.not_in(zodiac_signs))
    dp.include_router(router)
