from fastapi import FastAPI
from app.user.auth import router as auth_router
from app.user.router import router as user_router
from app.main_function.routers.posts import router as posts_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(posts_router)
