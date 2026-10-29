from dataclasses import dataclass


@dataclass
class Inventory:
    inventory_id: int
    name: str
    type: str
    status: str
    quantity: int
