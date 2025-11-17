from uuid import UUID

from sqlalchemy import select, or_, update
from sqlalchemy.orm import selectinload

from app.database.base_dao import BaseDAO
from app.database.models import Chat, Messange
from app.database.engine import async_session_maker

class ChatDAO(BaseDAO):
    model=Chat
    
    @classmethod
    async def get_or_create_chat(cls, user1 : int, user2 : int):
        async with async_session_maker() as session:
            request = select(cls.model).where(
                or_(
                    (cls.model.user1 == user1) & (cls.model.user2 == user2),
                    (cls.model.user1 == user2) & (cls.model.user2 == user1)
                )
            ).options(
                selectinload(cls.model.user1),
                selectinload(cls.model.user2)
            )
            
            result = await session.execute(request)
            chat = result.scalar_one_or_none()
            
            if not chat:
                user1, user2 = sorted([user1, user2])
                chat = cls.model(user1_id=user1, user2_id=user2)
                await session.add(chat)
                await session.commit()
                
                request2 = select(cls.model).where(
                    cls.model.id == chat.id
                ).options(
                    selectinload(cls.model.user1),
                    selectinload(cls.model.user2)
                )
                result = await session.execute(request2)
                chat = result.scalar_one()
            
            return chat
        
    @classmethod
    async def get_chats(cls, user : int):
        async with async_session_maker() as session:
            request = select(cls.model).where(
                or_(
                    cls.model.user1_id == user,
                    cls.model.user2_id == user
                )
            )
            
            result = await session.execute(request)
            return result.mappings().all()
        

class MessangeDAO(BaseDAO):
    model = Messange
    
    
    @classmethod
    async def add(cls, chat_id: int, sender_id: int, content: str):
        async with async_session_maker() as session:
            message = cls.model(
                chat_id=chat_id,
                from_id=sender_id,
                content=content,
            )
            
            session.add(message)
            await session.commit()
            await session.refresh(message)
            
            return message
    
    @classmethod
    async def get_chat_messange(cls, chat : int, limit : int = 100, offset : int = 0):
        async with async_session_maker() as session:
            request = select(cls.model).where(
                cls.model.chat_id==chat
            ).order_by(cls.model.date.asc()).limit(limit).offset(offset)
            
            result = await session.execute(request)
            return result.mappings().all()
        
    @classmethod
    async def get_by_uuid(cls, message_uuid: UUID):
        async with async_session_maker() as session:
            request = select(cls.model).where(cls.model.uuid == message_uuid)
            result = await session.execute(request)
            return result.scalar_one_or_none()
    
    @classmethod
    async def mark_as_read(cls, message_uuid: UUID):
        async with async_session_maker() as session:
            request = update(cls.model).where(
                cls.model.uuid == message_uuid
            ).values(is_read=True)
            
            await session.execute(request)
            await session.commit()
    
    @classmethod
    async def get_unread_count(cls, user: int, chat: int) -> int:
        async with async_session_maker() as session:
            request = select(cls.model).where(
                cls.model.chat_id == chat,
                cls.model.from_id != user,
                cls.model.is_read == False
            )
            
            result = await session.execute(request)
            return len(result.mappings().all())
        
    @classmethod
    async def make_all_chat_read(cls, chat_id : int, user_id):
         async with async_session_maker() as session:
            request = update(cls.model).where(
                cls.model.chat_id == chat_id,
                cls.model.from_id != user_id,
                cls.model.is_read == False
            ).values(is_read=True)
        
            await session.execute(request)
            await session.commit()