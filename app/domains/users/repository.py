from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from sqlalchemy.exc import SQLAlchemyError
from app.core.logging_info import app_logger

from typing import Optional

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self.db.get(User, user_id)

    async def get_by_username(self, username: str) -> Optional[User]:

        try:
            res = await self.db.execute(select(User).where(User.username == username))
            return res.scalar_one_or_none()
        except SQLAlchemyError as e:
            app_logger.error("Query failed with: {e}", exc_info=True)
            raise

    async def create(self, user: User) -> User:
        
        try:
            self.db.add(user)
            await self.db.commit()

        except SQLAlchemyError as e:
            app_logger.error("Query failed with: {e}", exc_info=True)
            raise

        await self.db.refresh(user)
        return user
