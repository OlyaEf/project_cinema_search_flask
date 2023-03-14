from project.models import Genre, Director, User
from typing import List, Optional, TypeVar
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.models import Movie
from project.setup.db.models import Base
from .base import BaseDAO


T = TypeVar('T', bound=Base)


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_by_order(self, page: Optional[int] = None, status=None) -> List[T]:
        stmt = self._db_session.query(self.__model__)
        if status:
            stmt = stmt.order_by(desc(self.__model__.year))
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def get_by_login(self, login):
        return self._db_session.query(User).filter(User.email == login).first()

    def create(self, data: dict):
        try:
            data_user = User(
                data['email'],
                data['password'],
            )
            self._db_session.add(data_user)
            self._db_session.commit()
            print("User Created")
        except Exception as e:
            print("Error creating", e)
            self._db_session.rollback()

    def update_user(self, data: dict):

        self._db_session.add(data)
        self._db_session.commit()
        return data


