from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import UserDAO, HoroscopeDAO
from app.dao.message import MessageDAO


@dataclass
class HolderDao:
    session: AsyncSession
    user: UserDAO = field(init=False)
    message: MessageDAO = field(init=False)
    horoscope: HoroscopeDAO = field(init=False)

    def __post_init__(self) -> None:
        self.user = UserDAO(self.session)
        self.message = MessageDAO(self.session)
        self.horoscope = HoroscopeDAO(self.session)

    async def commit(self) -> None:
        await self.session.commit()
