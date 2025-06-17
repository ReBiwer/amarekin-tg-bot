from dishka import Provider, Scope, provide
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.database import async_session_maker


class DBSessionProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    async def get_user_dao(self) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
