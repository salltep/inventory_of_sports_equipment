from dataclasses import dataclass


@dataclass
class Operation:
    operation_id: int
    inventory_id: int
    user_id: int
    type: str
    date: str
    comment: str | None = None
