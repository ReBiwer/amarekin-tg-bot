from backend.models.user import User
from backend.db.dao.base import BaseDAO


class UserDAO(BaseDAO):
    model = User
