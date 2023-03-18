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
        # try:
        data_user = User(**data)
        self._db_session.add(data_user)
        self._db_session.commit()
        print("User Created")
        return data_user
        # except Exception as e:
        #     print("Error creating", e)
        #     self._db_session.rollback()

    def update_user(self, email, data: dict):
        user = self.get_by_login(email)

        if 'email' in data:
            user.email = data.get('email')
        if 'password' in data:
            user.password = data.get('password')
        if 'name' in data:
            user.name = data.get('name')
        if 'surname' in data:
            user.surname = data.get('surname')
        if 'favorite_genre' in data:
            user.favorite_genre = data.get('favorite_genre')
        if 'favorite_movie' in data:
            user.favorite_movie = data.get('favorite_movie')
        self._db_session.add(data)
        self._db_session.commit()
        return data
