from pydantic import BaseModel, ConfigDict
from typing import Optional

from uuid import UUID


class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    uuid: UUID
