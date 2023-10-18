from models.database_models import TimeTable
from repository.repository_base import RepositoryBase


class TimetableRepository(RepositoryBase):
    """Класс репозитория для работы с расписанием в БД."""

    def __init__(self, engine):
        super().__init__(engine, TimeTable)

    async def get_status_file_by_user_id(self, user_id: str) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(File.user_id == user_id))).scalars().all()

    async def update(self, model) -> None:
        values = dict(filter(lambda x: not x[0].startswith('_'), model.__dict__.items()))
        await self._execute_statement(
            self._get_subquery_update().filter(File.filename == model.filename).values(values)
        )

    async def get_status_file_by_filename(self, filename: str) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(File.filename == filename))).scalar_one_or_none()

    async def get_status_file_by_id_file(self, id: str) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(File.id == id))).scalar_one_or_none()