import uuid
from fastapi import APIRouter, Depends

from app.main_function.daos.comment_dao import CommentDAO
from app.main_function.daos.post_dao import PostDAO
from app.schemas import SComment, SPost
from app.user.dependencies import current_user
from app.HTTPExceptions import DBError


router = APIRouter(
    prefix="/post",
    tags=["Посты"]
)

@router.get("/")
async def get_all_posts():
    return await PostDAO.find_all()

@router.post("/add")
async def add_post(post_data : SPost, user : dict = Depends(current_user)) -> bool:
    response = await PostDAO.add(post_data.model_dump(), user)
    if not response:
        raise DBError
    

@router.patch("/like")
async def like(uuid : uuid.UUID) -> bool:
    response = await PostDAO.like(uuid = uuid)
    if not response:
        raise DBError
    
@router.post("/comment")
async def comment(data : SComment, user : dict = Depends(current_user)) -> bool:
    response = await CommentDAO.add(data.model_dump(), user)
    if not response:
        raise DBError
    
@router.get("/{uuid}")
async def get_one_post(uuid : uuid.UUID):
    return await PostDAO.find_by_id(uuid=uuid)