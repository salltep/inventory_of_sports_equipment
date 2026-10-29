from dataclasses import dataclass


@dataclass
class Damage:
    damage_id: int
    inventory_id: int
    description: str
    date: str
