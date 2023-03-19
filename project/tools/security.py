import base64
import hashlib
import hmac
from typing import Union

from flask import current_app


def __generate_password_digest(password: str) -> bytes:
    """
    Хэшируем пароль код без возможности разхэшировать.
    :param password: Строкой пароль.
    :return: Хэш в байтов виде.
    """
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    """
    Кодируем хэш в байтовом в строку используя схему base64.
    :param password: Хэш в байтовом виде.
    :return: Закодированную строку.
    """
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_password(password_hash: Union[str, bytes], other_password: str) -> bool:
    hash_digest = generate_password_hash(other_password)
    return password_hash == hash_digest
