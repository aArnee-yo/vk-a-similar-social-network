from fastapi import APIRouter, Depends, Response

from app.user.dao import UserDAO



router = APIRouter(
    prefix="/user",
    tags=["Пользователь"]
)

@router.get("/me")
async def get_me(id : int):
    return await UserDAO.find_by_id(model_id = id)



    
        