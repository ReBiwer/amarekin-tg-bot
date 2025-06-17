from dishka import Provider, Scope, provide
from typing import AsyncGenerator

from backend.db.database import async_session_maker
from backend.db.dao.user import UserDAO


class UserDAOProvider(Provider):
    user_dao = provide(UserDAO)

    @provide(scope=Scope.REQUEST)
    async def get_user_dao(self) -> AsyncGenerator[UserDAO]:
        async with async_session_maker() as session:
            try:
                yield UserDAO(session)
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
