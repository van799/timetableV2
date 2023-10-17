from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl


class AppSettings(BaseSettings):
    project_name: str = "File repository"
    project_host: str | HttpUrl = "127.0.0.1"
    project_port: int = 8080


app_settings = AppSettings()