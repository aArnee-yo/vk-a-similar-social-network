from typing import Dict
from datetime import datetime

from fastapi import APIRouter, Depends,\
    WebSocket,\
    WebSocketDisconnect,\
    WebSocketException

from app.main_function.daos.websocket_dao import ChatDAO, MessangeDAO
from app.main_function.websocet.meneger import meneger
from app.user.dependencies import current_user
from app.main_function.websocet.validator import *


router = APIRouter(
    prefix="/websocket",
    tags=["Вебсокет"]
)

@router.websocket("/")
async def messanger_websocket(websocket : WebSocket, user_id : int = Depends(current_user)):
    await meneger.connect(websocket=websocket, user_id=user_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            await handle_messange(user_id, data)
    except WebSocketDisconnect:
        meneger.disconnect(user_id=user_id)
    except WebSocketException as e:
        print(f"websocket error : {e}")
    except Exception as e:
        print(f"Another error : {e}")
        
async def handle_messange(user_id : int, data : Dict):
    type = data.get("type")
    
    try:
        if type == "send_message":
            message_data = PrivateMessageCreate(**data["data"])
            await send_messange(user_id, message_data)
            
        elif type == "typing":
            typing_data = TypingIndicator(**data["data"])
            await typing(user_id, typing_data)
            
        elif type == "read_receipt":
            receipt_data = ReadReceipt(**data["data"])
            await read_receipt(user_id, receipt_data)
            
    except Exception as e:
        await meneger.send_message({
            "type": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, user_id)
        
    
async def send_messange(user_id : int, data : PrivateMessageCreate):
    chat = await ChatDAO.get_or_create_chat(user_id, data.receiver_id)
    
    message = await MessangeDAO.add(
        chat_id=chat.id,
        sender_id=user_id,
        content=data.content
    )
    
    sender_response = {
        "type": "message_sent",
        "data": {
            "uuid": str(message.uuid),
            "chat_id": chat.id,
            "receiver_id": data.receiver_id,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "is_read": message.is_read
        },
        "timestamp": datetime.now().isoformat()
    }
    
    receiver_response = {
        "type": "new_message",
        "data": {
            "uuid": str(message.uuid),
            "chat_id": chat.id,
            "sender_id": user_id,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "is_read": message.is_read
        },
        "timestamp": datetime.now().isoformat()
    }
    
    await meneger.send_message(sender_response, user_id)
    await meneger.send_message(receiver_response, data.receiver_id)
    
    
async def typing(sender_id: int, typing_data: TypingIndicator):
    message = {
        "type": "user_typing",
        "data": {
            "user_id": sender_id,
            "is_typing": typing_data.is_typing
        },
        "timestamp": datetime.now().isoformat()
    }
    
    await meneger.send_message(message, typing_data.receiver_id)
    
async def read_receipt(user_id: int, receipt_data: ReadReceipt):
    await MessangeDAO.mark_as_read(receipt_data.message_uuid)
       
    message = await MessangeDAO.get_by_uuid(receipt_data.message_uuid)
    if message:
        read_notification = {
            "type": "message_read",
            "data": {
                "message_uuid": str(receipt_data.message_uuid),
                "reader_id": user_id
            },
            "timestamp": datetime.now().isoformat()
        }
        await meneger.send_message(read_notification, message.sender_id)
        