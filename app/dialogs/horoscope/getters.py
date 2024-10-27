from aiogram_dialog import DialogManager

from app.services.horoscope import get_zodiac_name, get_horoscope_by_zodiac_name, insert_horoscope


async def get_horoscope(dialog_manager: DialogManager, **kwargs):
    zodiac_name = await get_zodiac_name(dialog_manager)

    if zodiac_name not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["zodiac_name"] = zodiac_name

    horoscope = await get_horoscope_by_zodiac_name(zodiac_name)

    await insert_horoscope(dialog_manager, zodiac_name)

    return {
        "horoscope": horoscope
    }
