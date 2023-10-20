import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from api.v1.api import router
from core.app_settings import app_settings

app = FastAPI(
    title=app_settings.project_name,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router, prefix='')


"""Запуск сервера"""
if __name__ == "__main__":
    uvicorn.run(app,
                host=app_settings.project_host,
                port=app_settings.project_port,
                )
