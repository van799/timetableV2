from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status

router = APIRouter()

templates = Jinja2Templates(directory="static/templates")


@router.get("/",
            status_code=status.HTTP_201_CREATED,
            response_class=HTMLResponse,
            description='Главная страница')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/calendar",
            status_code=status.HTTP_201_CREATED,
            response_class=HTMLResponse,
            description='Календарь')
async def calendar(request: Request):
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
    return templates.TemplateResponse("calendar2.html", {"request": request, 'events': events})
