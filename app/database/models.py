import uuid as uid
import datetime as dt
from typing import List, Optional
from sqlalchemy import JSON, UUID, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.engine import Base


        
class Post(Base):
    __tablename__ = "posts"
    
    
    uuid : Mapped[uid.UUID] = mapped_column(UUID, primary_key=True, default=uid.uuid4, nullable=False, unique=True)
    owner_id : Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date : Mapped[dt.datetime] = mapped_column(nullable=False)
    content : Mapped[str] = mapped_column(Text, nullable=False)
    media : Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
    likes : Mapped[int] = mapped_column(nullable=False, default=0)
    
    owner: Mapped["User"] = relationship(
        back_populates="posts"
    )
    
    comments : Mapped[list["Comment"]] = relationship(
        back_populates="posts",
        lazy='selectin'
    )
    
    
class Comment(Base):
    __tablename__ = "comments"
    
    
    uuid : Mapped[uid.UUID] = mapped_column(UUID, primary_key=True, default=uid.uuid4, nullable=False)
    owner_id : Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    post : Mapped[uid.UUID] = mapped_column(ForeignKey("posts.uuid"), nullable=False)
    date : Mapped[dt.datetime] = mapped_column(nullable=False)
    content : Mapped[str] = mapped_column(Text, nullable=False)
    answer : Mapped[Optional[uid.UUID]] = mapped_column(ForeignKey("comments.uuid"), default=None, nullable=True)
    
    
    owner: Mapped["User"] = relationship(back_populates="comments")
    posts: Mapped["Post"] = relationship(back_populates="comments")
    
    parent_comment : Mapped[Optional["Comment"]] = relationship(
        "Comment",
        remote_side=[uuid],
        back_populates="replies",
        foreign_keys=[answer],
        lazy='selectin'
    )
    
    replies : Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="parent_comment",
        foreign_keys=[answer],
        lazy='selectin'
    )


class Chat(Base):
    __tablename__ = "chats"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    from_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    to_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    created : Mapped[dt.datetime] = mapped_column(default=dt.datetime.utcnow())
    
    user1 : Mapped["User"] = relationship(foreign_keys=[from_id])
    user2 : Mapped["User"] = relationship(foreign_keys=[to_id])
    messanges : Mapped[List["Messange"]] = relationship(back_populates="chat")
    
    
class Messange(Base):
    __tablename__ = "messanges"
    
    
    uuid : Mapped[uid.UUID] = mapped_column(UUID, primary_key=True, default=uid.uuid4(), unique=True)
    chat : Mapped[int] = mapped_column(ForeignKey("chats.id"))
    from_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    content : Mapped[str] = mapped_column(Text, nullable=False)
    date : Mapped[dt.datetime] = mapped_column(default=dt.datetime.utcnow())
    is_read : Mapped[bool] = mapped_column(default=False)
    
    chat: Mapped["Chat"] = relationship(back_populates="messanges")
    sender: Mapped["User"] = relationship()


class User(Base):
    __tablename__ = "users"
    
    
    id : Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    email : Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password : Mapped[str] = mapped_column(nullable=False)
    username : Mapped[str] = mapped_column(nullable=True, unique=True)
    first_name : Mapped[str] = mapped_column(nullable=True)
    last_name : Mapped[Optional[str]] = mapped_column()
    photo_link : Mapped[Optional[str]] = mapped_column()
    bio : Mapped[Optional[str]] = mapped_column()
    
    chats_as_user1: Mapped[list["Chat"]] = relationship(foreign_keys=[Chat.from_id])
    chats_as_user2: Mapped[list["Chat"]] = relationship(foreign_keys=[Chat.to_id])
    
    posts: Mapped[list["Post"]] = relationship(
        back_populates="owner",
        lazy="selectin"
    )
    
    comments : Mapped[list["Comment"]] = relationship(
        back_populates="owner",
        lazy='selectin'
    )