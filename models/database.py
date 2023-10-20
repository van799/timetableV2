import asyncio
import os
import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.app_settings import app_settings
from models.database_models import CommonBase


class Database:
    def __init__(self):
        if app_settings.is_debug:
            self.path = f'sql_app_{hash(datetime.time())}.db'
            self.SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///./{self.path}"
            self.engine = create_async_engine(
                self.SQLALCHEMY_DATABASE_URL, echo=True, future=True
            )
            self.async_session = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
            asyncio.run(self.metadate_create_all())
        else:
            self.engine = create_async_engine(app_settings.project_db, echo=app_settings.echo, future=True)

        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_session(self):
        await self.metadate_create_all()
        return AsyncSession(self.engine)

    async def metadate_create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(CommonBase.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session

    def dispose(self):
        self.remove_database_file()

    def remove_database_file(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def get_engine(self):
        return self.engine
