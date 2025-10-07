import datetime
from sqlalchemy import insert
from app.database.base_dao import BaseDAO
from app.database.models import Comment
from app.database.engine import async_session_maker


class CommentDAO(BaseDAO):
    model = Comment
    
    @classmethod
    async def add(cls, data : dict, user_data : dict):
        async with async_session_maker() as session:
            request = insert(cls.model).values(
                owner_id=user_data.id,
                post=data["post_uuid"],
                date=datetime.datetime.utcnow(),
                content=data["content"]
            )
            try:
                await session.execute(request)
                await session.commit()
            except Exception as e:
                return False
            finally:
                return True