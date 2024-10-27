from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    message_id: int
    chat_id: int
    db_id: int | None = None
    sent_at: datetime | None = None
