# app/domains/posts/router.py
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.domains.users.router import get_current_user

# router = APIRouter(prefix="/posts", tags=["posts"])


from fastapi import APIRouter, Depends
from app.domains.posts.service import PostService
from app.domains.posts.repository import PostRepository
from app.domains.users.repository import UserRepository
from pydantic import BaseModel
# from app.domains.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

class PostInput(BaseModel):
    caption: str

class CommentInput(BaseModel):
    text: str


# can you have a class to get reduandant code abstracted away?

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















# async def get_post_service(db: AsyncSession = Depends(get_db)):
#     repo = repository.PostRepository(db)
#     return service.PostService(repo)

# @router.post("", response_model=schemas.PostOut, status_code=status.HTTP_201_CREATED)
# async def create_post(post_in: schemas.PostCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
#     # ensure current user is owner
#     if current_user.id != post_in.user_id:
#         raise HTTPException(status_code=403, detail="Forbidden")
#     ps = service.PostService(repository.PostRepository(db))
#     return await ps.create_post(post_in)

# # issues with this 
# @router.get("/feed", response_model=List[schemas.PostOut])
# async def get_feed(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), limit: int = 20):
#     # gather followees
#     follow_repo = FollowRepository(db)
#     followees = await follow_repo.get_followees(current_user.id)
#     user_ids = followees + [current_user.id]
#     ps = service.PostService(repository.PostRepository(db))
#     return await ps.list_feed(user_ids, limit=limit)
