from datetime import datetime

from sqlalchemy import BigInteger, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from app.models.db import Base

from app.models import dto


class Horoscope(Base):
    __tablename__ = "horoscopes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    zodiac_sign: Mapped[str] = mapped_column(String, nullable=False)
    requested_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"<Horoscope ID={self.id} chat_id={self.chat_id} zodiac_sign={self.zodiac_sign} requested_at={self.requested_at}> "

    def to_dto(self) -> dto.Horoscope:
        return dto.Horoscope(
            db_id=self.id,
            chat_id=self.chat_id,
            zodiac_sign=self.zodiac_sign,
            requested_at=self.requested_at,
        )
