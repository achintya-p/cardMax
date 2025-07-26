import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from typing import Generator
from ..app.main import app
from ..app.config import get_settings
from ..app.db.database import Database
from ..app.auth import create_access_token

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_client():
    # Use test database
    settings = get_settings()
    test_db_name = f"{settings.database_name}_test"
    
    # Setup test database
    client = AsyncIOMotorClient(settings.mongodb_url)
    Database.client = client
    Database.db = client[test_db_name]
    
    # Create test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup
    await client.drop_database(test_db_name)
    client.close()

@pytest.fixture(scope="session")
def test_user_token():
    return create_access_token({"sub": "test@example.com"})

@pytest.fixture(scope="function")
async def clean_db():
    # Clean all collections before each test
    collections = await Database.db.list_collection_names()
    for collection in collections:
        await Database.db[collection].delete_many({})
    yield 