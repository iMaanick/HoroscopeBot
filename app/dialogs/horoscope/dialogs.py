import os

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.horoscope.getters import get_horoscope
from app.dialogs.utils import unknown_message_input
from app.states import Horoscope

src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))

horoscope_dialog = Dialog(
    Window(
        Format("{horoscope}"),
        StaticMedia(
            path=os.path.join(src_dir, "./images/zodiac.jpg"),
            type=ContentType.PHOTO,
        ),
        SwitchTo(Const("Обновить"), id="get_horoscope_update", state=Horoscope.get_horoscope),
        unknown_message_input,
        getter=get_horoscope,
        state=Horoscope.get_horoscope
    )
)
