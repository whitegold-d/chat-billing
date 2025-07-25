from pydantic import BaseModel

from app.infrastructure.db.model.response.user_response import UserResponseORM


class UserMetadataSchema(BaseModel):
    ...

class LoginResponseDTO(BaseModel):
    login: str
    display_name: str
    metadata: UserMetadataSchema

    @classmethod
    def from_orm(cls, user_response_orm: UserResponseORM) -> "LoginResponseDTO":
        return cls(
            login=user_response_orm.login,
            display_name=user_response_orm.name,
            metadata=UserMetadataSchema()
        )

class UserResponseSchemaDTO(BaseModel):
    id: str
    display_name: str
    metadata: UserMetadataSchema

    @classmethod
    def from_orm(cls, user_response_orm: UserResponseORM) -> "UserResponseSchemaDTO":
        return cls(
            id=str(user_response_orm.id),
            display_name=user_response_orm.name,
            metadata=UserMetadataSchema()
        )