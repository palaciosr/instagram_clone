# app/domains/posts/repository.py
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.posts.models import Post, Comment, Like
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.core.logging_info import app_logger

class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, caption: str):

        try:
            post = Post(user_id=user_id, caption=caption)
            self.db.add(post)
            await self.db.commit()
            await self.db.refresh(post) # two queries
            return post
        except SQLAlchemyError as e:
            app_logger.error("Query failed with: {e}", exc_info=True)
            raise

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

        try:
            result = await self.db.execute(q)
            return result.scalars().all()
        except SQLAlchemyError as e:
            app_logger.error("Query failed with: {e}", exc_info=True)
            raise

    async def like_post(self, post_id: int, user_id: int):
        
        try:
            like = Like(post_id=post_id, user_id=user_id)
            self.db.add(like)
            await self.db.commit()
            return like
        except SQLAlchemyError as e:
            app_logger.error("Query failed with: {e}", exc_info=True)

            raise 

    async def comment_post(self, post_id: int, user_id: int, text: str):

        try:
            com = Comment(post_id=post_id, user_id=user_id, text=text)
            self.db.add(com)
            await self.db.commit()
            return com
        
        except SQLAlchemyError as e:
            app_logger.error("Query failed with: {e}", exc_info=True)
            raise
