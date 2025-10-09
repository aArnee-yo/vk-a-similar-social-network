from datetime import datetime 
from uuid import UUID
from typing import Optional, List 
from pydantic import BaseModel, ConfigDict, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str
    
class SPostAdd(BaseModel):
    content: str
    media: Optional[List[str]] = None 
    
class SPost(BaseModel):
    uuid: UUID
    date: datetime 
    content: str
    media: Optional[List[str]] = None 
    likes: int
    first_name: str
    last_name: Optional[str] = None
    photo_link: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class SUserPost(BaseModel):
    uuid: UUID
    date: datetime 
    content: str
    media: Optional[List[str]] = None 
    likes: int
    
    model_config = ConfigDict(from_attributes=True)
    
class SOwner(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: Optional[str] = None
    photo_link: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class SComment(BaseModel):
    uuid: UUID
    owner: SOwner
    date: datetime
    content: str
    parent_comment_id: Optional[UUID] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class SPostForUUID(BaseModel):
    uuid: UUID
    owner_id: int
    date: datetime
    content: str
    media: Optional[List[str]] = None 
    likes: int
    owner: SOwner
    comments: Optional[List[SComment]] = None 
    
    model_config = ConfigDict(from_attributes=True)
    
class SUser(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: Optional[str] = None
    photo_link: Optional[str] = None
    bio: Optional[str] = None
    posts: Optional[List[SUserPost]] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class SCommentAdd(BaseModel):
    post_uuid: UUID
    content: str