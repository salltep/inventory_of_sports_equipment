from repositories import inventory_repository, operation_repository, user_repository
from services.constants import (MANAGER_ROLE_ID, OP_CHECK, OP_REPAIR, OP_WRITEOFF,
                                STATUS_REPAIR, STATUS_WRITTEN_OFF)


def list_inventory():
    return inventory_repository.get_all()


def add_inventory(manager_id: int, name: str, type_: str, quantity: int):
    manager = user_repository.get_by_id(manager_id)

    if not manager or manager.role_id != MANAGER_ROLE_ID:
        raise Exception("Только управляющий может добавлять инвентарь")

    if not name.strip():
        raise Exception("Название не может быть пустым")

    if not type_.strip():
        raise Exception("Тип не может быть пустым")

    if quantity < 1:
        raise Exception("Количество должно быть не меньше 1")

    items = inventory_repository.get_all()

    for i in items:
        if (
            i.name.lower() == name.strip().lower()
            and
            i.type.lower() == type_.strip().lower()
        ):
            raise Exception("Такой инвентарь уже существует")

    inventory_repository.create(name.strip(), type_.strip(), quantity)


def check_inventory(manager_id: int, inventory_id: int):
    manager = user_repository.get_by_id(manager_id)

    if not manager or manager.role_id != MANAGER_ROLE_ID:
        raise Exception("Только управляющий может проверять инвентарь")

    if not inventory_repository.get_by_id(inventory_id):
        raise Exception("Инвентарь не найден")

    operation_repository.create(
        inventory_id,
        manager_id,
        OP_CHECK,
        "Плановая проверка"
    )


def send_to_repair(manager_id: int, inventory_id: int):
    manager = user_repository.get_by_id(manager_id)

    if not manager or manager.role_id != MANAGER_ROLE_ID:
        raise Exception("Только управляющий может отправлять на ремонт")

    item = inventory_repository.get_by_id(inventory_id)

    if not item:
        raise Exception("Инвентарь не найден")

    if item.status == STATUS_WRITTEN_OFF:
        raise Exception("Списанный инвентарь нельзя отправить в ремонт")

    if item.status == STATUS_REPAIR:
        raise Exception("Инвентарь уже в ремонте")

    inventory_repository.update_status(inventory_id, STATUS_REPAIR)
    operation_repository.create(
        inventory_id,
        manager_id,
        OP_REPAIR,
        "Отправлено на ремонт"
    )


def write_off(manager_id: int, inventory_id: int):
    manager = user_repository.get_by_id(manager_id)

    if not manager or manager.role_id != MANAGER_ROLE_ID:
        raise Exception("Только управляющий может списывать инвентарь")

    item = inventory_repository.get_by_id(inventory_id)

    if not item:
        raise Exception("Инвентарь не найден")

    if item.status == STATUS_WRITTEN_OFF:
        raise Exception("Инвентарь уже списан")

    inventory_repository.update_status(inventory_id, STATUS_WRITTEN_OFF)
    operation_repository.create(
        inventory_id,
        manager_id,
        OP_WRITEOFF,
        "Списано"
    )
