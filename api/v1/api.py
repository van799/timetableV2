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


@router.post("/timetable",
             status_code=status.HTTP_201_CREATED,
             response_model=RequestMessage,
             description='Добавлене дежурств.')
async def timetable(*,
                    session: AsyncSession = Depends(Database.get_session),
                    request: UsersRegistration,
                    ):
    file_repository = TimetableRepository(session)
    timetable = TimeTable()
    timetable.type_duty = request.type_duty
    timetable.user = request.user
    timetable.data = request.data

    await file_repository.add(timetable)

    return RequestMessage(message='расписание обновлено')


# @router.post("/admin",
#              response_model=RequestMessage,
#              status_code=status.HTTP_201_CREATED,
#              description='Регистрация пользователя')
# async def register(*,
#                    session: AsyncSession = Depends(database.get_session),
#                    request: UsersRegistration
#                    ) -> Any:
#     user_authenticate = UserAuthenticator(session)
#
#     if await user_authenticate.register_user(request.username, request.password):
#         return RequestMessage(message='Пользователь успешно зарегистрировался')
#     return RequestMessage(message='Такой пользователь уже существует')
