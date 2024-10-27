import asyncio
import os

from aiogram import Dispatcher, Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, User, Chat
from aiogram_dialog import DEFAULT_STACK_ID, ShowMode, StartMode
from aiogram_dialog.manager.bg_manager import BgManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from app.dao.holder import HolderDao
from app.dialogs import setup_all_dialogs
from app.handlers import setup_handlers, setup_unknown_text
from app.middlewares import setup_middlewares
from app.models import create_pool
from app.states import Horoscope


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="start"),
        BotCommand(command="/update", description="update"),
        BotCommand(command="/change_zodiac", description="change_zodiac"),
        BotCommand(command="/clear_history", description="clear_history"),
    ]
    await bot.set_my_commands(commands)


async def daily_horoscope(bot: Bot, router: Router, dao: HolderDao):
    users = await dao.user.get_users_to_send_horoscope()
    for user in users:
        bg = BgManager(user=User(id=user.tg_id, is_bot=False, first_name=user.first_name),
                       chat=Chat(id=user.tg_id, type="private"),
                       bot=bot,
                       router=router,
                       intent_id=None,
                       stack_id=DEFAULT_STACK_ID)
        await bg.start(Horoscope.get_horoscope, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def main():
    load_dotenv()
    token = os.getenv('TOKEN')
    if not token:
        raise ValueError("TOKEN env variable is not set")

    dp = Dispatcher()
    pool = create_pool()
    await setup_middlewares(dp, pool)
    setup_handlers(dp)
    dialog_router = setup_all_dialogs(dp)
    setup_unknown_text(dp)

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode='HTML')
    )
    await set_commands(bot)
    print("started")

    async with pool() as session:
        dao = HolderDao(session)

    scheduler = AsyncIOScheduler()
    scheduler.configure(timezone="Europe/Moscow")
    scheduler.add_job(daily_horoscope, 'cron', hour=13, minute=29, id="send_horoscope", args=[bot, dialog_router, dao])
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
