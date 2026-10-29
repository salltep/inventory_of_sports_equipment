import hashlib

from repositories import user_repository


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate(login: str, password: str):
    user = user_repository.get_by_login(login.strip())

    if not user or user.password_hash != hash_password(password):
        return None

    return user
