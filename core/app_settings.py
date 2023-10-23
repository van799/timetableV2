from pydantic_settings import BaseSettings
from pydantic import HttpUrl, PostgresDsn


class AppSettings(BaseSettings):
    project_name: str = "File repository"
    project_host: str | HttpUrl = "127.0.0.1"
    project_port: int = 7070
    project_db: PostgresDsn | str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    echo: bool = True
    is_debug: bool = True
    access_token_expire_minutes: int = 120


app_settings = AppSettings()
