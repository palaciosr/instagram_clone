# app/domains/posts/router.py
from typing import List, Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.domains.users.router import get_current_user
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.domains.posts.service import PostService
from app.domains.posts.repository import PostRepository
from app.domains.users.repository import UserRepository
from pydantic import BaseModel

router = APIRouter(prefix="/posts", tags=["Posts"])

# files
# class PostInput(BaseModel):
#     caption: str
#     file : UploadFile = File(None)

class CommentInput(BaseModel):
    text: str

#image: Optional[UploadFile] = File(None)
@router.post("")
async def create_post(caption: Optional[str] = Form(None),                 # text field
    file: Optional[UploadFile] = File(None), current=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = PostService(PostRepository(db), UserRepository(db))

    if file is not None:
        return await svc.create_post(current.username, caption, file)
    
    else:
        return await svc.create_post(current.username, caption)

@router.get("/feed")
async def feed(db: AsyncSession = Depends(get_db)):
    svc = PostService(PostRepository(db), UserRepository(db))
    return await svc.feed()


@router.get("/{post_id}/image")
async def get_image(post_id, db: AsyncSession = Depends(get_db)):
    svc = PostService(PostRepository(db), UserRepository(db))
    return await svc.repo.get_image(post_id)


@router.post("/{post_id}/like")
async def like(post_id: int, current=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = PostService(PostRepository(db), UserRepository(db))
    return await svc.like(current.username, post_id)


@router.post("/{post_id}/comment")
async def comment(post_id: int, data: CommentInput, current=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = PostService(PostRepository(db), UserRepository(db))
    return await svc.comment(current.username, post_id, data.text)
