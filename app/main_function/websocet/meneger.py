from fastapi import WebSocket
from typing import Dict


class ChatMessange:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket : WebSocket, user_id : int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

        
    def disconnect(self, user_id : int):
        for user_id in self.active_connections:
            del self.active_connections[user_id]
            
    async def send_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except Exception:
                self.disconnect(user_id)
            

                
meneger = ChatMessange()
                