from services.constants import MANAGER_ROLE_ID, TRAINER_ROLE_ID
from ui.auth import login, register_trainer
from ui.manager_menu import manager_menu
from ui.trainer_menu import trainer_menu


def main():
    while True:
        print("\n===== Учёт спортивного инвентаря =====")
        print("1. Вход в систему")
        print("2. Регистрация тренера")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            user = login()

            if user and user.role_id == MANAGER_ROLE_ID:
                manager_menu(user)
            elif user and user.role_id == TRAINER_ROLE_ID:
                trainer_menu(user)

        elif choice == "2":
            register_trainer()

        elif choice == "0":
            break


if __name__ == "__main__":
    main()
