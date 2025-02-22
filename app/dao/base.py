from sqlalchemy import delete, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, TypeVar, Type, Generic

from app.models.db.base import Base


Model = TypeVar('Model', Base, Base)


class BaseDAO(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self) -> List[Model]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def get_by_id(self, id_: int) -> Model:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id_)
        )
        return result.scalar_one()

    def save(self, obj: Model) -> None:
        self.session.add(obj)

    async def delete_all(self) -> None:
        await self.session.execute(
            delete(self.model)
        )

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count(self.model.id))
        )
        return result.scalar_one()

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self, *objects) -> None:
        await self.session.flush(objects)
