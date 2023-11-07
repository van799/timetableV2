import random
from calendar import monthrange
from datetime import datetime, timedelta
from http.client import HTTPException
from typing import Dict

from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from core.authenticate_user.form.LoginForm import LoginForm
from models.database import Database
from models.database_models import TimeTable, Event
from repository.timetable_repository.event_repository import EventRepository
from repository.timetable_repository.timetable_repository import TimetableRepository

from fastapi.security import OAuth2PasswordRequestForm

from repository.user_repository.user_repository import UserRepository

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
    events_title = []
    events_data = []
    timetable_repository = TimetableRepository(session)
    event_repository = EventRepository(session)

    title_timetable = await event_repository.get_all()
    for data in title_timetable:
        events_title.append({
            'title': data.title,
        })
    data_timetable = await timetable_repository.get_all()
    for data in data_timetable:
        events_data.append({
            'start': data.start,
            'end': data.end,
            'title_name': (await event_repository.get_by_id(data.title_id)).title
        })
    events = events_title + events_data
    return templates.TemplateResponse("table/index.html",
                                      {"request": request,
                                       'events': events})


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @router.post("/register",
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


@router.get("/admin",
            status_code=status.HTTP_201_CREATED,
            response_class=HTMLResponse,
            description='Панель адмнистратора')
async def admin(*,
                session: AsyncSession = Depends(database.get_session),
                request: Request
                ):
    titles = []
    events = []
    timetable_repository = TimetableRepository(session)
    event_repository = EventRepository(session)

    title_timetable = await event_repository.get_all()
    for data in title_timetable:
        titles.append({
            'title': data.title,
        })
    data_timetable = await timetable_repository.get_all()
    for data in data_timetable:
        events.append({
            'start': data.start,
            'end': data.end,
            'title_name': (await event_repository.get_by_id(data.title_id)).title
        })

    return templates.TemplateResponse("table/admin.html",
                                      {"request": request,
                                       'events': events, 'titles': titles})


@router.get('/auto_generated')
async def auto_generated_timetable(*,
                                   session: AsyncSession = Depends(database.get_session)
                                   ):
    timetable_repository = TimetableRepository(session)
    event_repository = EventRepository(session)

    timetable = TimeTable()

    events = await event_repository.get_all()

    day_month = 0
    current_year = datetime.now().year
    current_month = datetime.now().month

    days = monthrange(current_year, current_month)[1]
    start = datetime.strptime(f'{current_year}-{current_month}-01', '%Y-%m-%d')

    list_data = [(start + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(days)]
    if len(events) != 0:
        while day_month < days:
            if day_month == 28:
                a = 1
            event = events[random.randint(0, len(events) - 1)]
            timetable.title_id = event.id
            timetable.start = list_data[day_month]
            day_month += 1
            await timetable_repository.add(timetable)

    return RedirectResponse(
        '/admin',
        status_code=status.HTTP_302_FOUND)


@router.post("/insert")
async def insert_timetable(*,
                           session: AsyncSession = Depends(database.get_session),
                           request: Request
                           ):
    timetable_repository = TimetableRepository(session)
    event_repository = EventRepository(session)

    timetable = TimeTable()

    form_data_table = await request.form()
    timetable.start = form_data_table['start']
    timetable.end = form_data_table['end']
    title = await event_repository.get_by_title(form_data_table['title'])
    timetable.title_id = title.id
    await timetable_repository.add(timetable)

    return RedirectResponse(
        '/admin',
        status_code=status.HTTP_302_FOUND)


@router.post("/update")
async def update_timetable(*,
                           session: AsyncSession = Depends(database.get_session),
                           request: Request
                           ):
    timetable_repository = TimetableRepository(session)
    event_repository = EventRepository(session)

    timetable = TimeTable()

    form_data_table = await request.form()

    await timetable_repository.delete_by_date(form_data_table['old_start'])

    event = await event_repository.get_by_title(form_data_table['title'])

    timetable.title_id = event.id
    timetable.start = form_data_table['start']
    if form_data_table['end'] is not None:
        timetable.end = form_data_table['end']

    await timetable_repository.add(timetable)


@router.post('/delete_task')
async def delete_task(*,
                      session: AsyncSession = Depends(database.get_session),
                      request: Request
                      ):
    timetable_repository = TimetableRepository(session)
    form_data_table = await request.form()

    timetables = await timetable_repository.get_all()
    for timetable in timetables:
        if form_data_table['data_delete'] in timetable.start:
            await timetable_repository.delete_by_date(timetable.start)
    return RedirectResponse(
        '/admin',
        status_code=status.HTTP_302_FOUND)


@router.post('/add_task')
async def add_task(*,
                   session: AsyncSession = Depends(database.get_session),
                   request: Request
                   ):
    event_repository = EventRepository(session)
    form_data_table = await request.form()
    event = Event()

    event.title = form_data_table['title']

    find_title = await event_repository.get_by_title(form_data_table['title'])
    if find_title is None:
        await event_repository.add(event)

    return RedirectResponse(
        '/admin',
        status_code=status.HTTP_302_FOUND)


@router.get("/login")
async def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("table/login.html", context)


@router.post("token")
def login_for_access_token(
        response: Response,
        session: AsyncSession = Depends(database.get_session),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, str]:
    user_repository = UserRepository(session)
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"username": user.username})

    # Set an HttpOnly cookie in the response. `httponly=True` prevents
    # JavaScript from reading the cookie.
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=f"Bearer {access_token}",
        httponly=True
    )
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}


@router.post("/auth/login", response_class=HTMLResponse)
async def login_post(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = RedirectResponse("/", status.HTTP_302_FOUND)
            login_for_access_token(response=response, form_data=form)
            form.__dict__.update(msg="Login Successful!")

            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)
