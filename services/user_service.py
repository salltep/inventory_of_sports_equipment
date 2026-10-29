from repositories import user_repository
from services.auth_service import hash_password
from services.constants import MANAGER_ROLE_ID, TRAINER_ROLE_ID


def _create_trainer(login: str, password: str):
    if not login.strip():
        raise Exception("Логин не может быть пустым")

    if not password.strip():
        raise Exception("Пароль не может быть пустым")

    if user_repository.get_by_login(login.strip()):
        raise Exception("Пользователь с таким логином уже существует")

    user_repository.create(
        login.strip(),
        hash_password(password),
        TRAINER_ROLE_ID
    )


def register_trainer(login: str, password: str):
    _create_trainer(login, password)


def add_trainer(manager_id: int, login: str, password: str):
    manager = user_repository.get_by_id(manager_id)

    if not manager or manager.role_id != MANAGER_ROLE_ID:
        raise Exception("Только управляющий может добавлять тренеров")

    _create_trainer(login, password)
