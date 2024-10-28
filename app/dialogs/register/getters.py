from aiogram_dialog import DialogManager

from app.dialogs.utils import zodiac_signs


async def get_zodiac_buttons(dialog_manager: DialogManager, **kwargs) -> dict[str,  list[tuple[str, str]]]:
    zodiac_buttons_data = []

    for zodiac_emoji, zodiac_name in zodiac_signs.items():
        zodiac_buttons_data.append((zodiac_emoji, zodiac_name))

    return {
        "zodiac_buttons": zodiac_buttons_data
    }