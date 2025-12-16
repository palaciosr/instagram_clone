# app/domains/posts/repository.py
import shutil
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.posts.models import Post, Comment, Like
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.core.logging_info import app_logger


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_image(self, file):
        """ Save image to static folder"""

        from pathlib import Path
        current_file = Path(__file__).resolve()
            
            # 2. Go up 3 levels to reach the 'instagram_clone' directory
            # .parent = posts, .parent.parent = domains, .parent.parent.parent = app
            # So we go to 'app' then into 'static/uploaded_images'
        project_root = current_file.parent.parent.parent
        upload_dir = project_root / "static" / "uploaded_images"
        
        # 3. Ensure the folder exists locally
        upload_dir.mkdir(parents=True, exist_ok=True)        
        full_path = upload_dir / file.filename

        try:
            await file.seek(0)  # Ensure we're at the start of the file

            with open(full_path, "wb+") as buffer:

                shutil.copyfileobj(file.file, buffer)
            return str(full_path)

        except Exception as e:
            app_logger.error("Failed to save image: {e}", exc_info=True)
            raise

    # do a migration to get rid of content
    async def create(self, user_id: int, caption: str, file=None):

        try:

            if file is not None:
                full_path = await self.save_image(file)

                try:                
                    post = Post(user_id=user_id, caption=caption, 
                                file_name=full_path)
                except Exception as e:
                    app_logger.error("Failed to read file: {e}", exc_info=True)
                    raise

            else:
                post = Post(user_id=user_id, caption=caption)
            self.db.add(post)
            await self.db.commit()
            await self.db.refresh(post) # two queries
            return {"success": True, "post_id": post.id}
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


# best to push it into the feed.. 
    async def get_image(self, post_id: int):
        from pathlib import Path
        import os
        from fastapi import HTTPException
        from fastapi.responses import FileResponse

        try:

            try:
                result = await self.db.execute(select(Post).where(Post.id == int(post_id)))
                post = result.scalar_one_or_none()
            except SQLAlchemyError as e:
                app_logger.error("Query failed with: {e}", exc_info=True)
                raise

            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            if not os.path.exists(post.file_name):
                raise HTTPException(status_code=404, detail="Image file missing on server")

            if post.file_name:
                return FileResponse(post.file_name)

            else:
            
                post.image_data = None

                return None
        
        except Exception as e:
            app_logger.error("Failed to retrieve image: {e}", exc_info=True)

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
