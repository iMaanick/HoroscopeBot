from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Select

from app.dao.holder import HolderDao
from app.dialogs.utils import zodiac_descriptions
from app.services.message import insert_message
from app.services.register import upsert_user
from app.states import Horoscope


async def on_zodiac_sign_selected(
        callback: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        zodiac_name: str
):
    bot: Bot = dialog_manager.middleware_data["bot"]
    dao: HolderDao = dialog_manager.middleware_data["dao"]

    await upsert_user(dialog_manager, zodiac_name, dao)

    bot_msg = await bot.send_message(callback.from_user.id, zodiac_descriptions[zodiac_name])

    await insert_message(bot_msg.message_id, callback.from_user.id, dao)

    await dao.commit()

    await dialog_manager.start(
        Horoscope.get_horoscope,
        data=
        {
            'zodiac_name': zodiac_name
        },
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND
    )
