from project.dao.base import BaseDAO
from project.models import Genre, Director, User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class UsersDAO(BaseDAO[User]):
    __model__ = User
