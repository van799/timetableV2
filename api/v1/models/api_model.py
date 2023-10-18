from pydantic import BaseModel


class UsersRegistration(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: str | None = None


class TimeTable1(BaseModel):
    type_duty: str
    data: str
    user_id: str


class RequestMessage(BaseModel):
    message: str