# project/models.py -- файл используется для определения схемы базы данных, которая будет использоваться в приложении.

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    trailer = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    genre = relationship("Genre")
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)
    director = relationship("Director")


class User(models.Base):
    __tablename__ = 'users'

    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    name = Column(String(100))
    surname = Column(String(100))
    favorite_genre_id = Column(Integer, ForeignKey(f'{Genre.__tablename__}.id'))
    favorite_genre = relationship("Genre")
    favorite_movie_id = Column(Integer, ForeignKey(f'{Movie.__tablename__}.id'))
    favorite_movie = relationship("Movie")
