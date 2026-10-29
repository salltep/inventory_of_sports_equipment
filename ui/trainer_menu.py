from services.damage_service import report_damage
from services.inventory_service import list_inventory
from services.operation_service import issue_equipment, return_equipment


def trainer_menu(user):
    while True:
        print(f"\n===== Тренер ({user.login}) =====")
        print("1. Просмотр инвентаря")
        print("2. Выдача оборудования")
        print("3. Приём оборудования")
        print("4. Фиксация поломки")
        print("0. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                for i in list_inventory():
                    print(f"{i.inventory_id}. {i.name} ({i.type}) - "
                          f"{i.status}, количество: {i.quantity}")

            elif choice == "2":
                inventory_id = int(input("ID инвентаря: "))
                quantity = int(input("Количество: "))
                issue_equipment(user.user_id, inventory_id, quantity)
                print("Оборудование выдано")

            elif choice == "3":
                inventory_id = int(input("ID инвентаря: "))
                quantity = int(input("Количество: "))
                return_equipment(user.user_id, inventory_id, quantity)
                print("Оборудование принято")

            elif choice == "4":
                inventory_id = int(input("ID инвентаря: "))
                description = input("Описание поломки: ")
                report_damage(user.user_id, inventory_id, description)
                print("Поломка зафиксирована")

            elif choice == "0":
                break

            else:
                print("Неверный пункт меню")

        except ValueError:
            print("Ошибка: нужно ввести число")
        except Exception as e:
            print(f"Ошибка: {e}")
