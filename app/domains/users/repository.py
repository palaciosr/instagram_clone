from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User

from typing import Optional

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
            return await self.db.get(User, user_id)

    async def get_by_username(self, username: str) -> Optional[User]:
        
        res = await self.db.execute(select(User).where(User.username == username))
        return res.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user


