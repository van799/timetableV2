from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.app_settings import app_settings
from models.database_models import Users
from repository.user_repository.user_repository import UserRepository


class UserAuthenticator:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, session: AsyncSession):
        self.__session = session

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return UserAuthenticator.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return UserAuthenticator.pwd_context.hash(password)

    async def register_user(self, username: str, password: str):
        user_repository = UserRepository(self.__session)

        find_user = (await user_repository.get_user_by_name(username))
        if find_user is None:
            user = Users()
            user.username = username
            user.hashed_password = UserAuthenticator.get_password_hash(password)
            await user_repository.add(user)
            return True
        return False

    async def authenticate_user(self, username: str, password: str):
        user_repository = UserRepository(self.__session)
        user = await user_repository.get_user_by_name(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    async def create_access_token(user, expires_delta: timedelta = 15):
        user_dict = {
            "username": user.username,
            "password": user.hashed_password
        }
        if expires_delta:
            expire = datetime.utcnow() + expires_delta

        user_dict.update({"exp": expire})
        encoded_jwt = jwt.encode(user_dict, app_settings.secret_key, algorithm=app_settings.algorithm)
        return encoded_jwt

    @staticmethod
    async def get_current_user(session: AsyncSession, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token,
                                 app_settings.secret_key,
                                 algorithms=[app_settings.algorithm])
            username: str = payload.get("username")
        except JWTError:
            raise credentials_exception

        user_repository = UserRepository(session)
        user = await user_repository.get_user_by_name(username)

        if user is None:
            raise credentials_exception
        return user