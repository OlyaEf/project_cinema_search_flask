import calendar
import datetime

import jwt

from .users_serviece import UsersService
from ..config import BaseConfig

from typing import Optional

from project.exceptions import ItemNotFound
from project.models import User
from ..tools.security import compare_password

from flask import abort


class AuthService:
    def __init__(self, user_service: UsersService) -> None:
        self.user_service = user_service

    def get_item(self, pk: int) -> User:
        if user := self.user_service.get_item(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.user_service.get_all(page=page)

    def get_by_email(self, email):
        return self.user_service.get_by_email(email)

    def generate_tokens(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)

        if user is None:
            raise abort(404, 'user not found')

        if not is_refresh:
            if not compare_password(user.password, password):
                abort(400, 'wrong password')

        data = {
            "email": user.email,
        }

        # TOKEN_EXPIRE_MINUTES
        min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=BaseConfig.TOKEN_EXPIRE_MINUTES)
        data['exp'] = calendar.timegm(min15.timetuple())
        access_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.JWT_ALGORITHM)

        # TOKEN_EXPIRE_DAYS
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=BaseConfig.TOKEN_EXPIRE_DAYS)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.JWT_ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=BaseConfig.SECRET_KEY, algorithms=[BaseConfig.JWT_ALGORITHM])
        user_email = data.get("email")

        if user_email is None:
            raise Exception('')

        return self.generate_tokens(user_email, password=None, is_refresh=True)
