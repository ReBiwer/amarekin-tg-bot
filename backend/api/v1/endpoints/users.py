from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

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
        user_dao: FromDishka[UserDAO],
) -> UserResponse:
    new_user = await user_dao.add(user)
    return UserResponse.model_validate(new_user)
