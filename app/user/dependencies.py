import datetime
from fastapi import Request, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.user.dao import UserDAO
from app.HTTPExceptions import tokenAncorrect, tokenExpired, userNotFound


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password : str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data : dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.KEY, settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(data : dict, day : int = 60) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(days=day)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.REFRESH_KEY, settings.ALGORITHM
    )
    return encoded_jwt

def get_token(request : Request):
    token = request.cookies.get("vk_access_token")
    if not token:
        raise tokenAncorrect
    return token

def get_refresh_token(request : Request):
    refresh = request.cookies.get("vk_refresh_token")
    if not refresh:
        raise tokenAncorrect
    return refresh



async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not (user and verify_password(password, user.hashed_password)):
        return None
    
    return user 

async def current_user(token : str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.KEY, settings.ALGORITHM
        )
    except JWTError:
        raise tokenAncorrect
    expire : str = payload.get("exp")
    if not expire or int(expire)<datetime.datetime.utcnow().timestamp():
        raise tokenExpired
    user_id : str = payload.get("sub")
    if not user_id:
        raise userNotFound
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise userNotFound
    
    return user

async def refresh_user(token : str = Depends(get_refresh_token)):
    try:
        payload = jwt.decode(
            token, settings.REFRESH_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise tokenAncorrect
    expire : str = payload.get("exp")
    if not expire or int(expire)<datetime.datetime.utcnow().timestamp():
        raise tokenExpired
    user_id : str = payload.get("sub")
    if not user_id:
        raise userNotFound
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise userNotFound
    
    return user_id