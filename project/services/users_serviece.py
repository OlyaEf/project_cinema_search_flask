
from typing import Optional

from project import dao
from project.dao import UsersDAO
from project.exceptions import ItemNotFound
from project.models import User


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

    # def create(self, data):
    #     data['email'] = dao.create(data['email'])
    #     data['password'] = self.dao.create(generate_password_hash(data['password']))
    #     self.dao.create(data)
    #
    # def update(self, data):
    #     data['email'] = dao.create(data['email'])
    #     data['password'] = self.dao.create(generate_password_hash(data['password']))
    #     self.dao.update_user(data)


