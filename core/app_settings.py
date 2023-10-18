from pydantic_settings import BaseSettings
from pydantic import HttpUrl, PostgresDsn


class AppSettings(BaseSettings):
    project_name: str = "File repository"
    project_host: str | HttpUrl = "127.0.0.1"
    project_port: int = 7070
    project_db: PostgresDsn | str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )
    echo: bool = True
    is_debug: bool = True


app_settings = AppSettings()
