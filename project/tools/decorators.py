import jwt


from flask import request, abort

from project.config import BaseConfig


def auth_required(func):
    """
    Декоратор, проверяющий наличие заголовка Authorization и правильность JWT-токена.

    :param func: функция, к которой будет применен декоратор
    :return: функция-обертка, проверяющая наличие заголовка Authorization и правильность JWT-токена
    """
    def wrapper(*args, **kwargs):
        """
        Функция-обертка, проверяющая наличие заголовка Authorization и правильность JWT-токена.

        :param args: позиционные аргументы, передаваемые в функцию-обертку
        :param kwargs: именованные аргументы, передаваемые в функцию-обертку
        :return: результат выполнения функции, к которой был применен декоратор, если JWT-токен верный
        """
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(jwt=token, key=BaseConfig.SECRET_KEY, algorithms=[BaseConfig.JWT_ALGORITHM])
        except Exception as e:
            print('JWT Decode Exception', e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper



