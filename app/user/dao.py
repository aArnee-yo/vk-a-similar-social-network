from sqlalchemy import select
from app.database.base_dao import BaseDAO
from app.database.engine import async_session_maker
from app.database.models import User


class UserDAO(BaseDAO):
    model = User
    
    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session_maker() as session:
            request = select(cls.model).filter_by(id=model_id)
            result = await session.execute(request)
            result : dict = result.scalar_one_or_none()
            return result