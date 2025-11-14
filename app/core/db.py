import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import DATABASE_URL


# echo is for debugging
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_db():#AsyncSession
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as e:
        print("Error occurred while getting DB session:", e)
        raise
