from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum

class Category(str, Enum):
    DINING = "dining"
    TRAVEL = "travel"
    GROCERIES = "groceries"
    GAS = "gas"
    ENTERTAINMENT = "entertainment"
    ONLINE_SHOPPING = "online_shopping"
    OTHER = "other"

class RewardType(str, Enum):
    CASHBACK = "cashback"
    POINTS = "points"
    MILES = "miles"

class Card(BaseModel):
    id: str
    name: str
    issuer: str
    rewards: Dict[Category, float]
    reward_type: RewardType
    annual_fee: float = 0.0
    foreign_transaction_fee: float = 0.0
    sign_up_bonus: Optional[str] = None

class UserWallet(BaseModel):
    user_id: str
    cards: List[Card]

class InputQuery(BaseModel):
    category: Category
    amount: float = Field(..., gt=0)
    foreign_transaction: bool = False

class CardRecommendation(BaseModel):
    card: Card
    reward_value: float
    explanation: str 