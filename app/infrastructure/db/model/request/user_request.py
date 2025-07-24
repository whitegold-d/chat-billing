from dataclasses import dataclass


@dataclass
class UserRequestORM:
    login: str
    name: str
    hashed_password: str