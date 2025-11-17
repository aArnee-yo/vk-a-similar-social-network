from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class PrivateMessageCreate(BaseModel):
    receiver_id: int
    content: str
    
class TypingIndicator(BaseModel):
    receiver_id: int
    is_typing: bool

class ReadReceipt(BaseModel):
    message_uuid: UUID
    receiver_id: int
    
class PrivateMessageResponse(BaseModel):
    uuid: UUID
    chat_id: int
    sender_id: int
    receiver_id: int
    content: str
    created_at: datetime
    is_read: bool