from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.user.auth import router as auth_router
from app.user.router import router as user_router
from app.main_function.routers.posts import router as posts_router
from app.main_function.websocet.websocket import router as websocket_router
from app.main_function.routers.messanger import router as chat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(posts_router, prefix="/api", tags=["posts"])
app.include_router(websocket_router, prefix="/api", tags=["websocket"])
app.include_router(chat_router, prefix="/api", tags=["chat"])


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Social Network API", "docs": "/docs"}
