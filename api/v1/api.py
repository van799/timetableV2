from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.v1.models.api_model import RequestMessage, UsersRegistration, TimeTable1
from models.database import Database
from models.database_models import TimeTable
from repository.timetable_repository.timetable_repository import TimetableRepository

router = APIRouter()
database = Database()
templates = Jinja2Templates(directory="static/templates")


@router.get("/",
            status_code=status.HTTP_201_CREATED,
            response_class=HTMLResponse,
            description='Главная страница')
async def index(request: Request):
    events = [
        {
            'todo': 'Hello world',
            'date': '2023-10-17'
        },
        {
            'todo': 'Hello world',
            'date': '2023-10-18'
        },
    ]
    return templates.TemplateResponse("table/index.html", {"request": request, 'events': events})


@router.get("/admin",
            status_code=status.HTTP_201_CREATED,
            response_class=HTMLResponse,
            description='Панель адмнистратора')
async def index(request: Request):
    return templates.TemplateResponse("table/admin.html", {"request": request})


@router.post("/admin",
             status_code=status.HTTP_201_CREATED,
             response_class=HTMLResponse,
             description='Панель адмнистратора')
async def index(request: Request):
    print(request.data)

# @router.post("/admin",
#              status_code=status.HTTP_201_CREATED,
#              response_model=RequestMessage,
#              description='Добавлене дежурств.')
# async def timetable(*,
#                     session: AsyncSession = Depends(database.get_session),
#                     request: TimeTable1,
#                     ):
#     file_repository = TimetableRepository(session)
#     timetable = TimeTable()
#     timetable.type_duty = request.type_duty
#     timetable.user_id = request.user_id
#     timetable.data = request.data
#
#     await file_repository.add(timetable)
#
#     return templates.TemplateResponse("table/admin.html", {"request": request})
