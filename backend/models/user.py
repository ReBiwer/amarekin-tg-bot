from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column, Mapped
from backend.db.database import Base


class User(Base):
    username: Mapped[str]
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    first_name: Mapped[str | None]
