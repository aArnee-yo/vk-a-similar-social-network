from fastapi import APIRouter, Depends, Response

from app.user.dao import UserDAO
from app.database.models import User  
from app.user.dependencies import \
    create_access_token,\
    create_refresh_token,\
    get_password_hash,\
    authenticate_user,\
    refresh_user
from app.schemas import SUserAuth
from app.HTTPExceptions import userAlreadyReg, userNotFound, DBError


router = APIRouter(
    prefix="",
    tags=["Аунтефикация и Авторизация"]
)

@router.post("/auth")
async def register(user : SUserAuth) -> bool:
    existing_user = await UserDAO.find_one_or_none(email=user.email)
    if existing_user:
        raise userAlreadyReg
    hashed_password = get_password_hash(user.password)
    response = await UserDAO.add(email=user.email, hashed_password=hashed_password)
    if not response:
        raise DBError
    return True


@router.post("/login")
async def login(response : Response, user_data : SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    
    if not user:
        raise userNotFound
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    response.set_cookie(
        "vk_access_token", 
        access_token, 
        httponly=True,
        secure=True,
        samesite="lax"
    )
    response.set_cookie(
        "vk_refresh_token", 
        refresh_token, 
        httponly=True,
        secure=True, 
        samesite="lax"
    )
    
    return {"message": "Login successful", "user_id": user.id}

@router.post("/logout")
async def logout(response : Response):
    response.delete_cookie("vk_access_token")
    response.delete_cookie("vk_refresh_token")
    return {"message": "Logout successful"}

@router.post("/refresh")
async def refresh_access_token(response : Response, user : str = Depends(refresh_user)):
    access_token = create_access_token({"sub" : user})
    response.set_cookie("vk_access_token", access_token, httponly=True)
    return {"message": "Refresh successful"}

    
        