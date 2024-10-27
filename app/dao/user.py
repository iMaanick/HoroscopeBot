from datetime import datetime, timedelta

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.models.db import User, Horoscope
from app.models import dto


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_tg_id(self, tg_id: int) -> dto.User:
        result = await self.session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        return result.scalar_one().to_dto()

    async def upsert_user(self, user: dto.User) -> dto.User:
        kwargs = dict(
            tg_id=user.tg_id,
            first_name=user.first_name,
            zodiac_sign=user.zodiac_sign
        )
        saved_user = await self.session.execute(
            insert(User)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(User.tg_id,), set_=kwargs, where=User.tg_id == user.tg_id
            )
            .returning(User)
        )
        return saved_user.scalar_one().to_dto()

    async def get_users_to_send_horoscope(self) -> list[dto.User]:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        subquery = (
            select(Horoscope.chat_id)
            .where(Horoscope.requested_at >= today_start, Horoscope.requested_at < today_end)
            .group_by(Horoscope.chat_id)
            .subquery()
        )

        query = (
            select(User)
            .where(User.tg_id.not_in(select(subquery.c.chat_id)))
        )

        result = await self.session.execute(query)
        users = result.scalars().all()
        return [user.to_dto() for user in users]
