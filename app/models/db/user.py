from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from app.models import dto
from app.models.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str]
    zodiac_sign: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        rez = (
            f"<User "
            f"ID={self.tg_id} "
            f"name={self.first_name}"
            f"zodiac_sign={self.zodiac_sign}"
        )

        return rez + ">"

    def to_dto(self) -> dto.User:
        return dto.User(
            db_id=self.id,
            tg_id=self.tg_id,
            first_name=self.first_name,
            zodiac_sign=self.zodiac_sign,

        )
