import uuid
from fastapi import APIRouter, Depends

from app.main_function.daos.comment_dao import CommentDAO
from app.main_function.daos.post_dao import PostDAO
from app.schemas import SComment, SCommentAdd, SPost, SPostAdd, SPostForUUID
from app.user.dependencies import current_user
from app.HTTPExceptions import DBError, postNotFound


router = APIRouter(
    prefix="/post",
    tags=["Посты"]
)

@router.get("/")
async def get_all_posts() -> list[SPost]:
    result =  await PostDAO.find_all()
    if not result:
        raise postNotFound
    return result

@router.post("/add")
async def add_post(post_data : SPostAdd, user : dict = Depends(current_user)) -> bool:
    response = await PostDAO.add(post_data.model_dump(), user)
    if not response:
        raise DBError
    return True
    

@router.patch("/like")
async def like(uuid : uuid.UUID) -> bool:
    response = await PostDAO.like(uuid = uuid)
    if not response:
        raise DBError
    return True
    
@router.post("/comment")
async def comment(data : SCommentAdd, user : dict = Depends(current_user)) -> bool:
    response = await CommentDAO.add(data.model_dump(), user)
    if not response:
        raise DBError
    return True
    
@router.get("/{uuid}")#debagit nado
async def get_one_post(uuid : uuid.UUID) -> SPostForUUID:
    result =  await PostDAO.find_by_id(uuid=uuid)
    if not result:
        raise postNotFound
    return result