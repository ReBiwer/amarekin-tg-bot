import logging
from sqlalchemy import select, exists
from sqlalchemy.exc import SQLAlchemyError

from backend.models.user import User
from backend.db.dao.base import BaseDAO
from backend.schemas.user import UserBase
from backend.core.config import settings

logger = logging.getLogger(settings.NAME_LOGGER)


class UserDAO(BaseDAO):
    model = User

    async def add_or_get(self, values: UserBase):
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f"Добавление записи {self.model.__name__} с параметрами: {values_dict}")
        try:
            new_instance = self.model(**values_dict)
            query_exists = select(
                exists().where(
                    self.model.telegram_id == values.telegram_id
                )
            )
            exists_instance = await self._session.execute(query_exists)
            if not exists_instance.scalar():
                self._session.add(new_instance)
                logger.info(f"Запись {self.model.__name__} успешно добавлена.")
                await self._session.flush()
                return new_instance
            instance = await self._session.execute(
                select(self.model).where(self.model.telegram_id == values.telegram_id)
            )
            return instance.scalar_one()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении записи: {e}")
            raise
