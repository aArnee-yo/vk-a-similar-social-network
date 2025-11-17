from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.user.dependencies import current_user
from app.main_function.daos.websocket_dao import ChatDAO, MessangeDAO
from app.main_function.websocet.validator import PrivateMessageCreate, PrivateMessageResponse
from app.database.models import User
from app.HTTPExceptions import chatNotFound

router = APIRouter(
    prefix="/chat",
    tags=["Чаты"]
)

@router.get("/chats")
async def get_my_chats(current_user: User = Depends(current_user)) -> List[dict]:
    chats = await ChatDAO.get_chats(current_user.id)
    
    result = []
    for chat in chats:
        if chat.user1_id == current_user.id:
            partner = chat.user2
        else:
            partner = chat.user1
        
        last_message = await MessangeDAO.get_chat_messages(chat.id, limit=1)
        
        result.append({
            "chat_id": chat.id,
            "partner": {
                "id": partner.id,
                "username": partner.username,
                "first_name": partner.first_name,
                "photo_link": partner.photo_link
            },
            "last_message": last_message[0] if last_message else None,
            "unread_count": await MessangeDAO.get_unread_count(current_user.id, chat.id),
            "created_at": chat.created_at
        })
    
    return result

@router.get("/chats/{chat_id}/messages", response_model=List[PrivateMessageResponse])
async def get_chat_messages(
    chat_id: int,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(current_user)
):
    chat = await ChatDAO.find_by_id(chat_id)
    if not chat or (chat.user1_id != current_user.id and chat.user2_id != current_user.id):
        raise chatNotFound
    
    return await MessangeDAO.get_chat_messages(chat_id, limit, offset)

@router.post("/send")
async def send_private_message(
    message_data: PrivateMessageCreate,
    current_user: User = Depends(current_user)
):
    chat = await ChatDAO.get_or_create_chat(current_user.id, message_data.receiver_id)
    
    message = await MessangeDAO.add(
        chat_id=chat.id,
        sender_id=current_user.id,
        content=message_data.content
    )
    
    return message

@router.post("/chats/{chat_id}/read")
async def mark_chat_as_read(
    chat_id: int,
    current_user: User = Depends(current_user)
):
    chat = await ChatDAO.find_by_id(chat_id)
    if not chat or (chat.user1_id != current_user.id and chat.user2_id != current_user.id):
        raise chatNotFound
    MessangeDAO.make_all_chat_read(chat_id, current_user.id)
    return {"status": "all messages marked as read"}