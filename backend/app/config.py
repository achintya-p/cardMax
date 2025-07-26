from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    api_version: str = "1.0.0"
    debug: bool = False
    
    # Database Settings
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "cardmax"
    
    # Redis Settings
    redis_url: str = "redis://localhost:6379"
    
    # JWT Settings
    jwt_secret_key: str = "your-super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # ML Model Settings
    model_path: str = "models"
    min_training_samples: int = 100
    personalization_weight: float = 0.2
    
    # Cache Settings
    cache_ttl: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings() 