from repositories import damage_repository, inventory_repository, user_repository
from services.constants import STATUS_WRITTEN_OFF, TRAINER_ROLE_ID


def report_damage(trainer_id: int, inventory_id: int, description: str):
    trainer = user_repository.get_by_id(trainer_id)

    if not trainer or trainer.role_id != TRAINER_ROLE_ID:
        raise Exception("Только тренер может фиксировать поломки")

    if not description.strip():
        raise Exception("Описание поломки не может быть пустым")

    item = inventory_repository.get_by_id(inventory_id)

    if not item:
        raise Exception("Инвентарь не найден")

    if item.status == STATUS_WRITTEN_OFF:
        raise Exception("Инвентарь уже списан")

    damage_repository.create(inventory_id, description.strip())
