from pydantic import BaseModel, ConfigDict
from typing import Optional

from uuid import UUID


class UserBase(BaseModel):
    telegram_id: int
    username: str
    first_name: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    uuid: UUID
