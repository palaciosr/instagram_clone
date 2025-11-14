# app/domains/posts/repository.py
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.posts.models import Post, Comment, Like
from typing import List


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, caption: str):
        post = Post(user_id=user_id, caption=caption)
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def get_feed(self):
        # only loads users feed?

        q = (
            select(Post)
            # 1. Eagerly load the Post.user relationship
            .options(selectinload(Post.user))# users 
            
            # 2. Eagerly load the Post.likes collection
            .options(selectinload(Post.likes))
            
            # 3. Eagerly load the Post.comments collection, 
            #    AND nest the loading of the Comment.user for each comment.
            .options(
                selectinload(Post.comments).selectinload(Comment.user)
                # selectinload(Post.comments).selectinload("user")

            )
            .order_by(Post.created_at.desc())
        )

        
        result = await self.db.execute(q)
        return result.scalars().all()

    async def like_post(self, post_id: int, user_id: int):
        like = Like(post_id=post_id, user_id=user_id)
        self.db.add(like)
        await self.db.commit()
        return like

    async def comment_post(self, post_id: int, user_id: int, text: str):
        com = Comment(post_id=post_id, user_id=user_id, text=text)
        self.db.add(com)
        await self.db.commit()
        return com



    # async def list_by_user_ids(self, user_ids: List[int], limit: int = 20):
    #     if not user_ids:
    #         return []
    #     stmt = select(Post).where(Post.user_id.in_(user_ids)).order_by(desc(Post.created_at)).limit(limit)
    #     res = await self.db.execute(stmt)
    #     return res.scalars().all()

    # async def get(self, post_id: int) -> Post:
    #     return await self.db.get(Post, post_id)
