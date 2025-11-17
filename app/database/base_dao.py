from sqlalchemy import select, insert
from app.database.engine import async_session_maker



class BaseDAO:
    
    model = None
    
    @classmethod
    async def find_one_or_none(cls, **filter):
        async with async_session_maker() as session:
            request = select(cls.model).filter_by(**filter)
            result = await session.execute(request)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session_maker() as session:
            request = select(cls.model).filter_by(id=model_id)
            result = await session.execute(request)
            return result.scalar_one_or_none()
        
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            request = insert(cls.model).values(**data)
            try:
                await session.execute(request)
                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                return False
            
    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            request = select(cls.model)
            result = await session.execute(request)
            return result.mappings.all()
    