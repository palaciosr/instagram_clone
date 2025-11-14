import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.db import Base, get_db
from app.main import app

# Use an in-memory SQLite for async testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=True)
AsyncSessionTest = async_sessionmaker(engine_test, expire_on_commit=False)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True, scope="session")
async def setup_db():
    # Import all models so Base.metadata includes them
    import app.domains.users.models
    import app.domains.posts.models
    import app.domains.follows.models

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine_test.dispose()

@pytest.fixture()
async def db_session():
    async with AsyncSessionTest() as session:
        yield session

# Override dependency in FastAPI
app.dependency_overrides[get_db] = lambda: AsyncSessionTest()

@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
