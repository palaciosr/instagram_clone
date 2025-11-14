from app.domains.users.repository import UserRepository
from app.core.security import verify_password
from app.domains.auth.jwt import create_access_token

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def login(self, username: str, password: str):
        user = await self.repo.get_by_username(username)

        if not user:
            raise ValueError("Invalid username or password")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid username or password")

        token = create_access_token({"sub": user.username})

        return {"access_token": token, "token_type": "bearer"}
