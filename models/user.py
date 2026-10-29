from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    login: str
    password_hash: str
    role_id: int
