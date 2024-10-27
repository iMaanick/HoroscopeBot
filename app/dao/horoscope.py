from datetime import datetime, timedelta

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao import BaseDAO
from app.models import dto
from app.models.db.horoscope import Horoscope


class HoroscopeDAO(BaseDAO[Horoscope]):
    def __init__(self, session: AsyncSession):
        super().__init__(Horoscope, session)

    async def insert_horoscope(self, horoscope: dto.Horoscope) -> dto.Horoscope:
        kwargs = dict(
            chat_id=horoscope.chat_id,
            zodiac_sign=horoscope.zodiac_sign,
            requested_at=horoscope.requested_at
        )
        saved_horoscope = await self.session.execute(
            insert(Horoscope)
            .values(**kwargs)
            .returning(Horoscope)
        )
        return saved_horoscope.scalar_one().to_dto()

    async def get_chat_ids_and_zodiacs_not_today(self) -> list[dto.Horoscope]:
        today = datetime.now().date()
        result = await self.session.execute(
            select(Horoscope)
            .where(Horoscope.requested_at < today)
        )
        horoscopes = result.scalars().all()
        return [horoscope.to_dto() for horoscope in horoscopes]
