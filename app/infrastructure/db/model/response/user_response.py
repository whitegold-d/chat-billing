from dataclasses import dataclass
from uuid import UUID

@dataclass
class UserResponse:
    id: UUID
    login: str
    name: str
    hashed_password: str