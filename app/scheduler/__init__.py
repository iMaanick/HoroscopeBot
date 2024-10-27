from aiogram import Bot, Router
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.dao.holder import HolderDao
from app.scheduler.tasks import daily_horoscope


async def setup_scheduler(bot: Bot, router: Router, dao: HolderDao):
    scheduler = AsyncIOScheduler()
    scheduler.configure(timezone="Europe/Moscow")
    scheduler.add_job(daily_horoscope, 'cron', hour=10, minute=0, id="send_horoscope", args=[bot, router, dao])
    scheduler.start()