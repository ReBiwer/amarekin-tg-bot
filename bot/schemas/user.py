from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    telegram_id: int
    username: str
    first_name: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )
