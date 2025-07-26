from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from ..config import get_settings
from typing import Optional

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect_db(cls):
        """Create database connection."""
        settings = get_settings()
        cls.client = AsyncIOMotorClient(settings.mongodb_url)
        cls.db = cls.client[settings.database_name]
        
        # Create indexes
        await cls.db.users.create_index("email", unique=True)
        await cls.db.cards.create_index("name")
        await cls.db.transactions.create_index("user_id")
        await cls.db.ml_model_metadata.create_index("model_name", unique=True)

    @classmethod
    async def close_db(cls):
        """Close database connection."""
        if cls.client is not None:
            cls.client.close()

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if cls.db is None:
            raise ConnectionError("Database not initialized")
        return cls.db

# Database dependency
async def get_database() -> AsyncIOMotorDatabase:
    return Database.get_db() 