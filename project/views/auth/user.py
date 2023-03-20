from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user
from project.tools.decorators import auth_required

api = Namespace('users')


@api.route('/')
class UsersView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    @auth_required
    def get(self):
        """
        Get user(token).
        :return: token
        """
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        return user_service.get_from_token(token)

    @auth_required
    def patch(self):
        """
        User data updated
        :return: cod 200
        """
        token = request.headers['Authorization'].split('Bearer ')[-1]
        data_user = request.json
        user_service.update_user(token, data_user)
        return 'user data updated', 200


@api.route('/password/')
class UserView(Resource):
    @auth_required
    def put(self):
        """
        Password updated
        :return: cod 200 if successful else 404
        """
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        user = user_service.get_from_token(token)
        data_passwords = request.json
        if data_passwords['password_1'] == data_passwords['password_2']:
            user_service.update_password({'password': data_passwords['password_1']}, user.email)
            return 'password updated', 200
        else:
            return 'error password updated', 400
