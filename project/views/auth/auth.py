from importlib.resources import Resource

from flask_restx import Namespace
from flask import request

from project.container import auth_service, user_service
from project.setup.api.models import user


api = Namespace('auth')


@api.route('/register')
class AuthsView(Resource):
    @api.marshal_with(user, code=200, description='OK')
    def post(self):
        """
        We pass the email address and password, create a user in the system.
        """
        data = request.json
        login = data.get('email', None)
        password = data.get('password', None)
        if None in [login, password]:
            return 'user not created', 400

        user_ = user_service.create(data)

        return 'user created', 201, {'location': f'/user/{user_.id}'}


@api.route('/login')
class AuthsView(Resource):
    @api.marshal_with(user, code=200, description='OK')
    def post(self):
        """
        We send email and password and, if the user is authenticated,
        we return a response to the user in the form json.
        :return: {
           "access_token": "qwesfsdfa",
           "refresh_token": "kjhgfgjakda",
        }
        """
        data = request.json

        login = data.get('email', None)
        password = data.get('password', None)

        if None is [login, password]:
            return '', 400

        tokens = auth_service.generate_tokens(login, password)

        return tokens, 201

    @api.marshal_with(user, code=200, description='OK')
    def put(self):
        data = request.json
        token = data.get('refresh_token')

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201

