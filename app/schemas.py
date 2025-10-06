import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email : EmailStr
    password : str
    
class SPost(BaseModel):
    content : str
    media : Optional[list[str]]
    
class SComment(BaseModel):
    post_uuid : UUID
    content : str