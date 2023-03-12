from typing import List, Optional, TypeVar
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.models import Movie
from project.setup.db.models import Base
from .base import BaseDAO

T = TypeVar('T', bound=Base)


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
