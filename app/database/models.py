import uuid as uid
import datetime as dt
from typing import Optional
from sqlalchemy import JSON, UUID, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.engine import Base



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
    
    posts: Mapped[list["Post"]] = relationship(
        back_populates="owner",
        lazy="selectin"
    )
    
    comments : Mapped[list["Comment"]] = relationship(
        back_populates="owner",
        lazy='selectin'
    )
        
class Post(Base):
    __tablename__ = "posts"
    
    
    uuid : Mapped[uid.UUID] = mapped_column(primary_key=True, default=uid.uuid4, nullable=False, unique=True)
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
    
    
    uuid : Mapped[uid.UUID] = mapped_column(primary_key=True, default=uid.uuid4, nullable=False)
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
    
