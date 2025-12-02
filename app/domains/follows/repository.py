# app/domains/follows/repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.follows.models import Follow
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from app.core.logging_info import app_logger


class FollowRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def follow(self, follower_id: int, followee_id: int) -> Follow:

        try:
            exists = await self.db.execute(
            select(Follow).where(Follow.follower_id == follower_id, Follow.followee_id == followee_id)
        )

            if exists.scalar_one_or_none():
                return None
            
            f = Follow(follower_id=follower_id, followee_id=followee_id)
            self.db.add(f)
            
            await self.db.commit()

        except SQLAlchemyError as e:
            app_logger.error("Query failed with: {e}", exc_info=True)
            raise

        await self.db.refresh(f)
        return f

    async def get_followees(self, user_id: int) -> List[int]:

        try:
            res = await self.db.execute(select(Follow.followee_id).where(Follow.follower_id == user_id))
            return [r for (r,) in res.all()]
        except SQLAlchemyError as e:
            app_logger.error("Query failed with: {e}", exc_info=True)
            raise
