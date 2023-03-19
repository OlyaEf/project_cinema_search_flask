from typing import Optional

import jwt

from project.config import BaseConfig
from project.dao import UsersDAO
from project.exceptions import ItemNotFound
from project.models import User

from project.tools.security import generate_password_hash


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def get_email_from_token(self, token):
        data = jwt.decode(jwt=token, key=BaseConfig.SECRET_KEY, algorithms=[BaseConfig.JWT_ALGORITHM])
        user_email = data.get('email')
        return user_email

    def get_from_token(self, token):
        user_email = self.get_email_from_token(token)
        user = self.get_by_email(email=user_email)
        return user

    def create(self, data):
        data['password'] = generate_password_hash(data['password'])
        print(data)
        return self.dao.create(data)

    def update_user(self, token, user_data):
        email = self.get_email_from_token(token)
        self.dao.update_user(email, user_data)

    def update_password(self, data, email):
        print(data)
        data['password'] = generate_password_hash(data['password'])
        self.dao.update_user(email, data)

