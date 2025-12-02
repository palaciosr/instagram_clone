# app/domains/posts/router.py
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.domains.users.router import get_current_user

from fastapi import APIRouter, Depends
from app.domains.posts.service import PostService
from app.domains.posts.repository import PostRepository
from app.domains.users.repository import UserRepository
from pydantic import BaseModel

router = APIRouter(prefix="/posts", tags=["Posts"])

class PostInput(BaseModel):
    caption: str

class CommentInput(BaseModel):
    text: str


@router.post("")
async def create_post(data: PostInput, current=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = PostService(PostRepository(db), UserRepository(db))
    return await svc.create_post(current.username, data.caption)


@router.get("/feed")
async def feed(db: AsyncSession = Depends(get_db)):
    svc = PostService(PostRepository(db), UserRepository(db))
    return await svc.feed()


@router.post("/{post_id}/like")
async def like(post_id: int, current=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = PostService(PostRepository(db), UserRepository(db))
    return await svc.like(current.username, post_id)


@router.post("/{post_id}/comment")
async def comment(post_id: int, data: CommentInput, current=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = PostService(PostRepository(db), UserRepository(db))
    return await svc.comment(current.username, post_id, data.text)
