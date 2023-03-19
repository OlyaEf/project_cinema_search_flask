from flask_restx import Namespace, Resource
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
        email = data.get('email', None)
        password = data.get('password', None)
        if None in [email, password]:
            return 'user not created', 400

        return user_service.create(data)


@api.route('/login')
class AuthsView(Resource):

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

        email = data.get('email', None)
        password = data.get('password', None)

        if None is [email, password]:
            return '', 400

        tokens = auth_service.generate_tokens(email, password)

        return tokens, 201

    def put(self):
        """
        We accept a couple of tokens and, if they are valid, we create a couple of new ones.
        :return: returns new tokens.
        """
        data = request.json
        token = data.get('refresh_token')

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201

