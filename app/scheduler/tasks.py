from aiogram import Bot, Router
from aiogram.types import User, Chat
from aiogram_dialog import DEFAULT_STACK_ID, StartMode, ShowMode
from aiogram_dialog.manager.bg_manager import BgManager

from app.dao.holder import HolderDao
from app.states import Horoscope


async def daily_horoscope(bot: Bot, router: Router, dao: HolderDao):
    users = await dao.user.get_users_to_send_horoscope()
    for user in users:
        bg = BgManager(user=User(id=user.tg_id, is_bot=False, first_name=user.first_name),
                       chat=Chat(id=user.tg_id, type="private"),
                       bot=bot,
                       router=router,
                       intent_id=None,
                       stack_id=DEFAULT_STACK_ID)
        await bg.start(
            Horoscope.get_horoscope,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.DELETE_AND_SEND
        )
