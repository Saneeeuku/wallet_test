from typing import Type

from pydantic import BaseModel
from sqlalchemy import select, insert, delete as sqla_delete, update
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_base import Base


class BaseRepository:
    model: Type[Base] = None
    schema: Type[BaseModel] = None

    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_filtered(self, *q_filter, **filters):
        query = select(self.model).filter(*q_filter).filter_by(**filters)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        try:
            result = result.scalars().one()
        except (NoResultFound, MultipleResultsFound) as e:
            raise e
        return self.schema.model_validate(result, from_attributes=True)

    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(stmt)
        except IntegrityError as e:
            raise e
        result = result.scalars().one()
        return self.schema.model_validate(result, from_attributes=True)

    async def edit(self, data: BaseModel, exclude_unset_and_none: bool = False, **filters):
        stmt = (
            update(self.model)
            .filter_by(**filters)
            .values(
                **data.model_dump(
                    exclude_unset=exclude_unset_and_none, exclude_none=exclude_unset_and_none
                )
            )
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return self.schema.model_validate(res.scalar_one(), from_attributes=True)

    async def delete(self, *q_filter, **filters):
        if filters:
            try:
                await self.get_one(**filters)
            except NoResultFound as e:
                raise e
        stmt = sqla_delete(self.model).filter(*q_filter).filter_by(**filters)
        await self.session.execute(stmt)
