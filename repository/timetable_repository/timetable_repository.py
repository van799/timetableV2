from models.database_models import TimeTable
from repository.repository_base import RepositoryBase
from sqlalchemy import select, update, insert


class TimetableRepository(RepositoryBase):
    """Класс репозитория для работы с расписанием в БД."""

    def __init__(self, engine):
        super().__init__(engine, TimeTable)

    async def update(self, model) -> None:
        values = dict(filter(lambda x: not x[0].startswith('_'), model.__dict__.items()))
        await self._execute_statement(
            self._get_subquery_update().filter(TimeTable.title == model.title).values(values)
        )

    async def get_by_title(self, title: str) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(TimeTable.title == title))).scalar_one_or_none()

    async def get_by_data(self, start: str) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(TimeTable.start == start))).scalar_one_or_none()

    async def get_by_id(self, id: str) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(TimeTable.id == id))).scalar_one_or_none()

    async def delete_by_date(self, start: str) -> None:
        await self._execute_statement(
            self._get_subquery_update().where(TimeTable.start == start).values(deleted=True)
        )
