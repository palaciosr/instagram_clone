
# app/api/router.py
from fastapi import APIRouter
from app.domains.users.router import router as users_router
from app.domains.posts.router import router as posts_router
from app.domains.follows.router import router as follows_router

from app.domains.auth.router import router as auth_router

api_router = APIRouter(prefix="/api")
api_router.include_router(users_router)
api_router.include_router(posts_router)
api_router.include_router(follows_router)
api_router.include_router(auth_router)
