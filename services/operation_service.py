from repositories import inventory_repository, operation_repository, user_repository
from services.constants import (OP_ISSUE, OP_RETURN, STATUS_OK, STATUS_WRITTEN_OFF,
                                TRAINER_ROLE_ID)


def issue_equipment(trainer_id: int, inventory_id: int, quantity: int):
    trainer = user_repository.get_by_id(trainer_id)

    if not trainer or trainer.role_id != TRAINER_ROLE_ID:
        raise Exception("Только тренер может выдавать оборудование")

    if quantity < 1:
        raise Exception("Количество должно быть не меньше 1")

    item = inventory_repository.get_by_id(inventory_id)

    if not item:
        raise Exception("Инвентарь не найден")

    if item.status != STATUS_OK:
        raise Exception("Оборудование недоступно для выдачи")

    if quantity > item.quantity:
        raise Exception(f"На складе только {item.quantity} шт.")

    inventory_repository.update_quantity(inventory_id, item.quantity - quantity)
    operation_repository.create(
        inventory_id,
        trainer_id,
        OP_ISSUE,
        f"Выдано {quantity} шт."
    )


def return_equipment(trainer_id: int, inventory_id: int, quantity: int):
    trainer = user_repository.get_by_id(trainer_id)

    if not trainer or trainer.role_id != TRAINER_ROLE_ID:
        raise Exception("Только тренер может принимать оборудование")

    if quantity < 1:
        raise Exception("Количество должно быть не меньше 1")

    item = inventory_repository.get_by_id(inventory_id)

    if not item:
        raise Exception("Инвентарь не найден")

    if item.status == STATUS_WRITTEN_OFF:
        raise Exception("Инвентарь списан")

    inventory_repository.update_quantity(inventory_id, item.quantity + quantity)
    operation_repository.create(
        inventory_id,
        trainer_id,
        OP_RETURN,
        f"Возвращено {quantity} шт."
    )
