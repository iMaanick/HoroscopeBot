from dataclasses import dataclass
from datetime import datetime


@dataclass
class Horoscope:
    zodiac_sign: str
    chat_id: int
    requested_at: datetime | None = None
    db_id: int | None = None
