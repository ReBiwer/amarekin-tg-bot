from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column, Mapped
from backend.db.database import Base


class User(Base):
    username: Mapped[str]
    password: Mapped[str]
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    email: Mapped[str | None]
