# app/domains/follows/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.domains.follows.repository import FollowRepository
from app.domains.users.router import get_current_user

router = APIRouter(prefix="/follows", tags=["follows"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def follow_user(payload: dict, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    followee_id = payload.get("followee_id")
    if not followee_id:
        raise HTTPException(status_code=400, detail="followee_id required")
    if current_user.id == followee_id:
        raise HTTPException(status_code=400, detail="cannot follow yourself")
    repo = FollowRepository(db)
    f = await repo.follow(current_user.id, followee_id)
    if not f:
        raise HTTPException(status_code=400, detail="already following")
    return {"status": "ok", "follow_id": f.id}
