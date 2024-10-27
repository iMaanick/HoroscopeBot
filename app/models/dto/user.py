from dataclasses import dataclass


@dataclass
class User:
    tg_id: int
    zodiac_sign: str
    first_name: str
    db_id: int | None = None

