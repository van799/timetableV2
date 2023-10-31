import random
from datetime import datetime, timedelta
from http.client import HTTPException
from typing import Any

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from api.v1.models.api_model import UsersRegistration, RequestMessage, Token
from core.app_settings import app_settings
from models.database import Database
from models.database_models import TimeTable
from repository.timetable_repository.timetable_repository import TimetableRepository
from repository.user_authenticator import UserAuthenticator

router = APIRouter()
database = Database()
templates = Jinja2Templates(directory="static/templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/",
            status_code=status.HTTP_201_CREATED,
            response_class=HTMLResponse,
            description='Главная страница')
async def index(*,
                session: AsyncSession = Depends(database.get_session),
                request: Request
                ):
    events = []
    timetable_repository = TimetableRepository(session)
    data_timetable = await timetable_repository.get_all()
    for data in data_timetable:
        events.append({
            'todo': data.title,
            'date': data.start
        }
        )

    return templates.TemplateResponse("table/index.html", {"request": request, 'events': events})


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register",
             response_model=RequestMessage,
             status_code=status.HTTP_201_CREATED,
             description='Регистрация пользователя')
async def register(*,
                   session: AsyncSession = Depends(database.get_session),
                   request: UsersRegistration
                   ) -> Any:
    user_authenticate = UserAuthenticator(session)

    if await user_authenticate.register_user(request.username, request.password):
        return RequestMessage(message='Пользователь успешно зарегистрировался')
    return RequestMessage(message='Такой пользователь уже существует')


@router.post("/auth", response_model=Token)
async def login_for_access_by_token(
        *,
        request: UsersRegistration,
        session: AsyncSession = Depends(database.get_session)
):
    user_authenticate = UserAuthenticator(session)

    user = await user_authenticate.authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=app_settings.access_token_expire_minutes)
    access_token = await UserAuthenticator.create_access_token(
        user, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/admin",
            status_code=status.HTTP_201_CREATED,
            response_class=HTMLResponse,
            description='Панель адмнистратора')
async def admin(*,
                session: AsyncSession = Depends(database.get_session),
                request: Request
                ):
    events = []
    timetable_repository = TimetableRepository(session)
    data_timetable = await timetable_repository.get_all()
    for data in data_timetable:
        events.append({
            'todo': data.title,
            'date': data.start
        }
        )
    return templates.TemplateResponse("table/admin.html", {"request": request, 'events': events})


@router.get('/tasks')
def find_all_tasks(request: Request):
    events = []
    list_name = ['name1', 'name2', 'name3', 'name4']
    start = datetime.strptime('2023-10-01', '%Y-%m-%d')
    end = datetime.strptime('2023-10-30', '%Y-%m-%d')

    list_data = [(start + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(0, (end - start).days)]
    for data in list_data:
        events.append({
            'todo': random.choice(list_name),
            'date': data
        }
        )
    return templates.TemplateResponse("table/admin.html", {"request": request, 'events': events})


@router.post("/insert")
async def insert_timetable(*,
                           session: AsyncSession = Depends(database.get_session),
                           request: Request
                           ):
    timetable_repository = TimetableRepository(session)
    timetable = TimeTable()
    form_data_table = await request.form()
    print(form_data_table['title'])
    print(form_data_table['start'])
    timetable.title = form_data_table['title']

    timetable.start = form_data_table['start']
    await timetable_repository.add(timetable)


@router.post("/update")
async def update_timetable(*,
                           session: AsyncSession = Depends(database.get_session),
                           request: Request
                           ):
    timetable_repository = TimetableRepository(session)
    timetable = TimeTable()
    form_data_table = await request.form()

    await timetable_repository.delete_by_date(form_data_table['old_start'])

    timetable.title = form_data_table['title']
    timetable.start = form_data_table['start']
    await timetable_repository.add(timetable)


@router.post('/delete_task')
async def delete_task(*,
                      session: AsyncSession = Depends(database.get_session),
                      request: Request
                      ):
    timetable_repository = TimetableRepository(session)
    form_data_table = await request.form()

    print(form_data_table['data_delete'])
    result = await timetable_repository.get_by_data(form_data_table['data_delete'])
    if result is not None:
        await timetable_repository.delete_by_date(form_data_table['data_delete'])
    return RedirectResponse(
        '/admin',
        status_code=status.HTTP_302_FOUND)
