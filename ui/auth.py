from services.auth_service import authenticate
from services.user_service import add_trainer as add_trainer_service
from services.user_service import register_trainer as register_trainer_service


def login():
    login_value = input("Логин: ")
    password_value = input("Пароль: ")

    user = authenticate(login_value, password_value)

    if not user:
        print("Неверный логин или пароль")
        return None

    return user


def register_trainer():
    login_value = input("Логин: ")
    password_value = input("Пароль: ")

    try:
        register_trainer_service(login_value, password_value)
        print("Регистрация прошла успешно")
    except Exception as e:
        print(f"Ошибка: {e}")


def add_trainer(user):
    login_value = input("Логин тренера: ")
    password_value = input("Пароль: ")

    try:
        add_trainer_service(user.user_id, login_value, password_value)
        print("Тренер добавлен")
    except Exception as e:
        print(f"Ошибка: {e}")
