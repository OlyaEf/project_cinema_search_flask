from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='триллер'),
})

director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Альфред Хичкок'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=255, example='Психо'),
    'description': fields.String(required=True, example='Психологический хоррор'),
    'trailer': fields.String(required=True, max_length=255, example='https://www.youtube.com/watch?v=QItO4YITn7Y'),
    'year': fields.Integer(required=True, example=1960),
    'rating': fields.Float(required=True, example=8.1),
    'genre_id': fields.Integer(example=1),
    'director_id': fields.Integer(example=1)
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example='ingenious_psycho@gmail.com'),
    'password': fields.String(required=True, example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiSm9obiIsInJvbGUiOiJ1c2VyIiwiZXhwIjoxNjc4MTg1NDc5fQ.ar2lIBXAPbm-vFv-Np8RfQP6I0domPbXMJdtSQyJBH0'),
    'name': fields.String(max_length=100, example='Альфред'),
    'surname': fields.String(max_length=100, example='Хичкок'),
    'favorite_genre': fields.String(max_length=100, example='триллер')
})

