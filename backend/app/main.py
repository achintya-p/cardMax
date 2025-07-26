from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from datetime import datetime

from .models import Card, UserWallet, InputQuery, CardRecommendation, Category
from .rewards import get_best_card, predict_category
from .ml_models import category_predictor
from .config import get_settings
from .db.database import Database, get_database
from .db.models import UserDB, CardDB, WalletDB, TransactionDB
from .auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_password_hash
)

# Initialize settings
settings = get_settings()

app = FastAPI(
    title="Credit Card Optimizer",
    description="API for optimizing credit card usage based on rewards and ML predictions",
    version=settings.api_version
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # Initialize database connection
    await Database.connect_db()
    
    # Initialize Redis cache
    redis = aioredis.from_url(settings.redis_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.on_event("shutdown")
async def shutdown():
    await Database.close_db()

@app.get("/")
async def root():
    return {"message": "Welcome to Credit Card Optimizer API"}

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users", response_model=UserDB)
async def create_user(
    email: str,
    password: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Check if user exists
    if await db.users.find_one({"email": email}):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    user = UserDB(
        email=email,
        hashed_password=get_password_hash(password)
    )
    await db.users.insert_one(user.dict(by_alias=True))
    return user

@app.post("/optimize", response_model=CardRecommendation)
async def optimize_card_choice(
    query: InputQuery,
    description: Optional[str] = None,
    current_user: UserDB = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    try:
        # If description is provided, predict category
        if description and not query.category:
            query.category = predict_category(description)
            
        recommendation = get_best_card(query, current_user.id)
        
        # Store the transaction for future training
        if description:
            transaction = TransactionDB(
                user_id=current_user.id,
                description=description,
                category=query.category,
                amount=query.amount,
                card_id=recommendation.card.id,
                reward_value=recommendation.reward_value
            )
            await db.transactions.insert_one(transaction.dict(by_alias=True))
            
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/cards", response_model=List[Card])
async def get_cards(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: UserDB = Depends(get_current_active_user)
):
    cards = await db.cards.find({"is_active": True}).to_list(length=100)
    return [Card(**card) for card in cards]

@app.post("/wallet", response_model=WalletDB)
async def create_wallet(
    wallet: UserWallet,
    current_user: UserDB = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Check if wallet exists
    existing_wallet = await db.wallets.find_one({"user_id": current_user.id})
    if existing_wallet:
        raise HTTPException(
            status_code=400,
            detail="Wallet already exists for this user"
        )
    
    # Create new wallet
    wallet_db = WalletDB(
        user_id=current_user.id,
        cards=[card.id for card in wallet.cards]
    )
    await db.wallets.insert_one(wallet_db.dict(by_alias=True))
    return wallet_db

@app.get("/wallet/{user_id}", response_model=WalletDB)
async def get_wallet(
    user_id: str,
    current_user: UserDB = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Only allow users to access their own wallet
    if str(current_user.id) != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to access this wallet")
        
    wallet = await db.wallets.find_one({"user_id": user_id})
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return WalletDB(**wallet)

@app.post("/transactions/train")
async def train_models(
    current_user: UserDB = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Train ML models using stored transaction data"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to train models")
        
    transactions = await db.transactions.find().to_list(length=None)
    
    if not transactions or len(transactions) < settings.min_training_samples:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough training data. Need at least {settings.min_training_samples} samples."
        )
        
    descriptions = [t["description"] for t in transactions]
    categories = [t["category"] for t in transactions]
    
    try:
        category_predictor.train(descriptions, categories)
        category_predictor.save()
        
        # Store model metadata
        await db.ml_model_metadata.update_one(
            {"model_name": "category_predictor"},
            {
                "$set": {
                    "version": settings.api_version,
                    "last_trained": datetime.utcnow(),
                    "training_samples": len(transactions),
                    "is_active": True
                }
            },
            upsert=True
        )
        
        return {"message": "Models trained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.get("/predict-category")
async def get_category_prediction(
    description: str,
    current_user: UserDB = Depends(get_current_active_user)
):
    """Predict spending category from transaction description"""
    try:
        category = predict_category(description)
        return {"category": category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}") 