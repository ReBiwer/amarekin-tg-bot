from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.user import UserCreate, UserResponse
from db.dao.user import UserDAO

router = APIRouter(
    prefix="/users",
    tags=["users"],
    route_class=DishkaRoute,
)

@router.post("/telegram/add")
async def add_user(
        user: UserCreate,
        db_session: FromDishka[AsyncSession],
) -> UserResponse:
    print(id(db_session))
    dao = UserDAO(db_session)
    new_user = await dao.add_or_get(user)
    return UserResponse.model_validate(new_user)
