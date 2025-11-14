
# app/domains/users/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.domains.users import schemas, repository, service
# from app.core.security import create_access_token, decode_token

from app.domains.auth.jwt import create_access_token, verify_token

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.shared.exceptions import ConflictError, UnauthorizedError

# seems to be the case that you have to import all the models/schemas/repositories/services used in the router 
# to get the async functions to work properly

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")

async def get_user_service(db: AsyncSession = Depends(get_db)):
    repo = repository.UserRepository(db)
    return service.UserService(repo)

@router.post("", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: schemas.UserCreate, svc: service.UserService = Depends(get_user_service)):
    try:
        user = await svc.register(user_in)
        return user
    except ConflictError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends(), svc: service.UserService = Depends(get_user_service)):
    try:
        user = await svc.authenticate_user(form_data.username, form_data.password)
    except UnauthorizedError:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(subject=user.username, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


# helper to get current user in other domains
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    # username = await check_payload(token)
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    repo = repository.UserRepository(db)
    user = await repo.get_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/me", response_model=schemas.UserOut)
async def read_me(current_user = Depends(get_current_user)):
    return current_user
