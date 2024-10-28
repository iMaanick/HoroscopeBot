import datetime

from aiogram_dialog import DialogManager
from aiogram import html

from app.dao.holder import HolderDao
from app.models import dto


async def get_zodiac_name(dialog_manager: DialogManager) -> str:
    if "zodiac_name" in dialog_manager.dialog_data:
        return dialog_manager.dialog_data.get("zodiac_name")

    if dialog_manager.start_data and isinstance(dialog_manager.start_data,
                                                dict) and "zodiac_name" in dialog_manager.start_data:
        return dialog_manager.start_data.get("zodiac_name")

    dao: HolderDao = dialog_manager.middleware_data["dao"]
    user = await dao.user.get_by_tg_id(dialog_manager.event.from_user.id)
    return user.zodiac_sign


async def get_horoscope_by_zodiac_name(zodiac_name: str) -> str:
    current_date = datetime.datetime.now()
    return f"Horoscope for {zodiac_name} for the date {html.bold(current_date)}"


async def insert_horoscope(dialog_manager: DialogManager, zodiac_name: str) -> None:
    dao: HolderDao = dialog_manager.middleware_data["dao"]
    horoscope_dto = dto.Horoscope(zodiac_sign=zodiac_name, chat_id=dialog_manager.event.from_user.id)
    await dao.horoscope.insert_horoscope(horoscope_dto)
    await dao.commit()
