from fastapi import APIRouter, Depends, HTTPException, status
from app.domains.auth.service import AuthService
from app.domains.users.repository import UserRepository
from app.core.db import get_db
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginInput(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(data: LoginInput, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(UserRepository(db))
    
    try:
        return await auth_service.login(data.username, data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
