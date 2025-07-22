from dataclasses import dataclass


@dataclass
class UserRequest:
    login: str
    name: str
    hashed_password: str