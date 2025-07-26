from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from bson import ObjectId
from ..models import Category, RewardType

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class DBModelBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

class UserDB(DBModelBase):
    email: str = Field(..., unique=True)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

class CardDB(DBModelBase):
    name: str
    issuer: str
    rewards: Dict[Category, float]
    reward_type: RewardType
    annual_fee: float = 0.0
    foreign_transaction_fee: float = 0.0
    sign_up_bonus: Optional[str] = None
    is_active: bool = True

class WalletDB(DBModelBase):
    user_id: PyObjectId
    cards: List[PyObjectId]  # References to CardDB ids
    is_active: bool = True

class TransactionDB(DBModelBase):
    user_id: PyObjectId
    description: str
    amount: float
    category: Category
    card_id: Optional[PyObjectId] = None
    reward_value: Optional[float] = None
    is_foreign: bool = False
    merchant: Optional[str] = None
    location: Optional[str] = None

class MLModelMetadataDB(DBModelBase):
    model_name: str
    version: str
    last_trained: datetime
    training_samples: int
    performance_metrics: Dict[str, float]
    is_active: bool = True 