from models.database_models import Users
from repository.repository_base import RepositoryBase


class UserRepository(RepositoryBase):
    """Класс репозитория для сохранения user в БД."""

    def __init__(self, engine):
        super().__init__(engine, Users)

    async def get_user_by_name(self, username: str) -> list:
        return (await self._execute_statement(
            self._get_subquery().filter(Users.username == username))).scalar_one_or_none()
