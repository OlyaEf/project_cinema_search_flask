

from typing import Optional

from project.dao.movie import MoviesDAO
from project.exceptions import ItemNotFound
from project.models import Movie


class MoviesService:
    def __init__(self, dao: MoviesDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> Movie:
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f'Movie with pk={pk} not exists.')

    def get_all_by_order(self, page: Optional[int] = None, status: Optional[str] = None) -> list[Movie]:
        return self.dao.get_all_by_order(page=page, status=status)
