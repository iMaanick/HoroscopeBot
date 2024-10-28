from datetime import datetime

from sqlalchemy import BigInteger, Integer, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from app.models import dto
from app.models.db import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(BigInteger)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"<Message ID={self.id} message_id={self.message_id} chat_id={self.chat_id} sent_at={self.sent_at}>"

    def to_dto(self) -> dto.Message:
        return dto.Message(
            db_id=self.id,
            message_id=self.message_id,
            chat_id=self.chat_id,
            sent_at=self.sent_at,
        )
