from abc import ABC
from typing import Any

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.sql.expression import Select

from models.database_models import CommonBase


class RepositoryBase(ABC):
    def __init__(self, session: AsyncSession, repository_type: type(CommonBase)):
        self.__session = session
        self.__repository_type = repository_type

    async def add(self, model) -> None:
        values = dict(filter(lambda x: not x[0].startswith('_'), model.__dict__.items()))
        await self._execute_statement(insert(self.__repository_type).values(values))

    async def get_all(self) -> list:
        return (await self._execute_statement(self._get_subquery())).scalars().all()

    async def get_by_id(self, model_id: int) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(self.__repository_type.id == model_id))).scalar()

    async def delete_by_id(self, model_id: int) -> None:
        await self._execute_statement(
            update(self.__repository_type).where(self.__repository_type.id == model_id).values(deleted=True)
        )

    async def count(self):
        return (await self._execute_statement(
            select(func.count()).select_from(self._get_subquery().subquery('t1')))).scalar()

    async def _execute_statement(self, statement: Any) -> list[Any]:
        if type(statement) is Select:
            result = await self.__session.execute(statement)
            return result

        result = await self.__session.execute(statement)
        if type(statement) is not Select:
            await self.__session.commit()
            return []
        return result

    def _get_subquery(self):
        return select(self.__repository_type).filter(self.__repository_type.deleted == False)

    def _get_subquery_update(self):
        return update(self.__repository_type).filter(self.__repository_type.deleted == False)

    async def _execute_statement_scalars(self, statement: Any) -> list[Any]:
        return (await self._execute_statement(statement)).scalars().all()

    async def _execute_statement_scalar(self, statement: Any) -> Any:
        return (await self._execute_statement(statement)).scalar()
