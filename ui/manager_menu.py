from services.inventory_service import (add_inventory, check_inventory,
                                        list_inventory, send_to_repair,
                                        write_off)
from ui.auth import add_trainer


def show_inventory():
    for i in list_inventory():
        print(f"{i.inventory_id}. {i.name} ({i.type}) - "
              f"{i.status}, количество: {i.quantity}")


def manager_menu(user):
    while True:
        print(f"\n===== Управляющий ({user.login}) =====")
        print("1. Добавление инвентаря")
        print("2. Списание инвентаря")
        print("3. Проверка инвентаря")
        print("4. Отправка на ремонт")
        print("5. Добавление тренера")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                name = input("Название: ")
                type_ = input("Тип: ")
                quantity = int(input("Количество: "))
                add_inventory(user.user_id, name, type_, quantity)
                print("Инвентарь добавлен")

            elif choice == "2":
                show_inventory()
                inventory_id = int(input("ID инвентаря для списания: "))
                write_off(user.user_id, inventory_id)
                print("Инвентарь списан")

            elif choice == "3":
                show_inventory()
                inventory_id = int(input("ID проверяемого инвентаря: "))
                check_inventory(user.user_id, inventory_id)
                print("Проверка записана")

            elif choice == "4":
                show_inventory()
                inventory_id = int(input("ID инвентаря для ремонта: "))
                send_to_repair(user.user_id, inventory_id)
                print("Инвентарь отправлен на ремонт")

            elif choice == "5":
                add_trainer(user)

            elif choice == "0":
                break

            else:
                print("Неверный пункт меню")

        except ValueError:
            print("Ошибка: нужно ввести число")
        except Exception as e:
            print(f"Ошибка: {e}")
