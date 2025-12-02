from app.api.router import api_router

from fastapi import FastAPI
from app.core.db import Base, engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# fix 
@asynccontextmanager
async def lifespan(app: FastAPI):
    import app.domains.users.models
    import app.domains.posts.models
    import app.domains.follows.models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("db connected on startup")
    yield

    await engine.dispose()
    print("db disposed on shutdown")


app = FastAPI(title="Async DDD Instagram Clone", lifespan=lifespan)
app.include_router(api_router)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",  # Common port for React/Vue frontends
    "http://127.0.0.1:8000",  # Alternative localhost IP
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   