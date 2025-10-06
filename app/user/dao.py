from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.base_dao import BaseDAO
from app.database.engine import async_session_maker
from app.database.models import Post, User


class UserDAO(BaseDAO):
    model = User
    
    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session_maker() as session:
            request = (
            select(User)
            .options(selectinload(User.posts))
            .where(User.id == model_id)
        )
        result = await session.execute(request)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        return {
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "photo_link": user.photo_link,
            "bio": user.bio,
            "posts": [
                {
                    "uuid": post.uuid,
                    "date": post.date,
                    "content": post.content,
                    "media": post.media,
                    "likes": post.likes
                }
                for post in user.posts
            ]
        }