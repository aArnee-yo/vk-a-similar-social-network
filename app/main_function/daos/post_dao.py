import datetime
import uuid as uid
from sqlalchemy import insert, select, desc, update
from app.database.base_dao import BaseDAO
from app.database.engine import async_session_maker
from app.database.models import Post, User

class PostDAO(BaseDAO):
    model=Post

    @classmethod
    async def add(cls, data : dict, user_data : dict):
        async with async_session_maker() as session:
            request = insert(cls.model).values(
                owner_id=user_data.id,
                date=datetime.datetime.utcnow(),
                content=data["content"],
                media=data.get("media"),
                likes=0
            )
            
            await session.execute(request)
            await session.commit()
            
            return True
            
    
    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            request = select(
                    Post.uuid,
                    Post.date,
                    Post.content,
                    Post.media,
                    Post.likes,
                    User.first_name,
                    User.last_name,
                    User.photo_link
                ).join(
                    User, Post.owner_id == User.id
                ).order_by(
                    Post.date.desc()
                )
            result = await session.execute(request)
            return result.mappings().all()
        
    @classmethod
    async def find_by_id(cls, uuid : uid.UUID):
        async with async_session_maker() as session:
            request = select(cls.model).where(cls.model.uuid==uuid)
            result = await session.execute(request)
            return result.scalar_one_or_none()
        
    @classmethod
    async def like(cls, uuid : uid):
        async with async_session_maker() as session:
            request = (
                update(cls.model)
                .where(cls.model.uuid == uuid)
                .values(likes=cls.model.likes + 1)
                .execution_options(synchronize_session="fetch")
            )
            try:
                result = await session.execute(request)
                await session.commit()
            except:
                return False
            
            if result.rowcount == 0:
                return False   
            return True
        
        