from .models import User
from .schemas import UserCreate
from app.core.security import get_password_hash, verify_password
from .repository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, user_in: UserCreate):
        existing = await self.repo.get_by_username(user_in.username)
        if existing:
            raise ValueError("Username already exists")
        user = User(
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
            display_name=user_in.display_name,
            bio=user_in.bio
        )
        return await self.repo.create(user)

    async def authenticate_user(self, username: str, password: str):
        user = await self.repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
