from models.database_models import Event
from repository.repository_base import RepositoryBase


class EventRepository(RepositoryBase):
    """Класс репозитория для работы с расписанием в БД."""

    def __init__(self, engine):
        super().__init__(engine, Event)

    async def update(self, model) -> None:
        values = dict(filter(lambda x: not x[0].startswith('_'), model.__dict__.items()))
        await self._execute_statement(
            self._get_subquery_update().filter(Event.title == model.title).values(values)
        )

    async def get_by_title(self, title: str) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(Event.title == title))).scalar_one_or_none()

    async def get_by_id(self, id: str) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(Event.id == id))).scalar_one_or_none()

    async def delete_by_title(self, title: str) -> None:
        await self._execute_statement(
            self._get_subquery_update().where(Event.title == title).values(deleted=True)
        )
