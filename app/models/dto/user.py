from __future__ import annotations
from dataclasses import dataclass

from aiogram import types as tg


@dataclass
class User:
    tg_id: int
    zodiac_sign: str
    first_name: str
    db_id: int | None = None

    # @classmethod
    # def from_aiogram(cls, user: tg.User) -> User:
    #     return cls(
    #         tg_id=user.id,
    #         first_name=user.first_name,
    #     )
