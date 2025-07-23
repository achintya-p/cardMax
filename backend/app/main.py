from fastapi import FastAPI, HTTPException
from typing import List
from .models import Card, UserWallet, InputQuery, CardRecommendation
from .rewards import get_best_card

app = FastAPI(
    title="Credit Card Optimizer",
    description="API for optimizing credit card usage based on rewards",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Credit Card Optimizer API"}

@app.post("/optimize", response_model=CardRecommendation)
async def optimize_card_choice(query: InputQuery):
    try:
        recommendation = get_best_card(query)
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/cards", response_model=List[Card])
async def get_cards():
    # TODO: Implement card listing logic
    return []

@app.post("/wallet", response_model=UserWallet)
async def create_wallet(wallet: UserWallet):
    # TODO: Implement wallet creation logic
    return wallet 