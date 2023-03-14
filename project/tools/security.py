import base64
import hashlib
import hmac
from ctypes import Union

from flask import current_app


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_password(password_hash: Union[str, bytes], other_password: str) -> bool:
    decoded_digest = base64.b64encode(password_hash)
    hash_digest = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=other_password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )
    return hmac.compare_digest(decoded_digest, hash_digest)

