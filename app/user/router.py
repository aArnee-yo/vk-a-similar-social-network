from fastapi import APIRouter, Depends, Response

from app.schemas import SUserPost
from app.user.dao import UserDAO
from app.HTTPExceptions import userNotFound



router = APIRouter(
    prefix="/user",
    tags=["Пользователь"]
)

@router.get("/me")
async def get_me(id : int) -> SUserPost:
    result =  await UserDAO.find_by_id(model_id = id)
    if not result:
        raise userNotFound
    return result



    
        