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

    def get_by_login(self, login):
        return self.dao.get_by_login(login)

    def get_from_token(self, token):
        data = jwt.decode(jwt=token, key=BaseConfig.SECRET_KEY, algorithm=BaseConfig.JWT_ALGORITHM)
        user_login = data.get('email')
        user = self.get_by_login(login=user_login)
        return user

    def create(self, data):
        data['password'] = generate_password_hash(data['password'])
        print(data)
        return self.dao.create(data)

    def update(self, data, email):
        data['password'] = generate_password_hash(data['password'])
        self.dao.update_user(email, data)
