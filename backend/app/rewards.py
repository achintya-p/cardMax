import json
from typing import List, Dict, Optional
from pathlib import Path
from fastapi_cache.decorator import cache
from .models import Card, InputQuery, CardRecommendation, Category
from .ml_models import category_predictor, recommender

@cache(expire=3600)
def load_card_data() -> List[Card]:
    """
    Load card data from JSON file with caching
    """
    data_path = Path(__file__).parent / "data" / "card_rewards.json"
    if not data_path.exists():
        return []
        
    with open(data_path) as f:
        data = json.load(f)
        return [Card(**card) for card in data["cards"]]

def predict_category(description: str) -> Category:
    """
    Predict spending category from transaction description
    """
    return category_predictor.predict(description)

def calculate_reward_value(card: Card, query: InputQuery) -> float:
    """
    Calculate the reward value for a specific card and purchase
    """
    reward_rate = card.rewards.get(query.category, card.rewards.get(Category.OTHER, 0))
    
    # Calculate base reward value
    reward_value = query.amount * (reward_rate / 100)
    
    # Subtract foreign transaction fee if applicable
    if query.foreign_transaction:
        reward_value -= query.amount * (card.foreign_transaction_fee / 100)
    
    # Apply any special category bonuses (could be expanded based on seasonal promotions)
    if query.category in [Category.DINING, Category.TRAVEL] and query.amount >= 100:
        reward_value *= 1.1  # 10% bonus on large dining/travel purchases
    
    return reward_value

def get_best_card(query: InputQuery, user_id: Optional[str] = None) -> CardRecommendation:
    """
    Determine the best card to use for a given purchase, optionally using personalized recommendations
    """
    cards = load_card_data()
    if not cards:
        raise ValueError("No cards available")

    best_card = None
    best_value = float('-inf')
    
    # Get personalized scores if user_id is provided
    personalized_scores = {}
    if user_id:
        personalized_scores = recommender.get_personalized_scores(user_id, cards)
    
    for card in cards:
        value = calculate_reward_value(card, query)
        
        # Apply personalization if available
        if user_id and card.id in personalized_scores:
            personalization_weight = 0.2  # Adjust this weight based on confidence in personalization
            value = value * (1 + personalization_weight * personalized_scores[card.id])
        
        if value > best_value:
            best_card = card
            best_value = value
    
    if not best_card:
        raise ValueError("Could not determine best card")
    
    # Update recommender system with the chosen card
    if user_id:
        recommender.update_embeddings(user_id, best_card.id, best_value)
    
    explanation = (
        f"Using {best_card.name} will earn you "
        f"{best_value:.2f} {best_card.reward_type.value} "
        f"on your {query.amount:.2f} {query.category} purchase"
    )
    
    if user_id and personalized_scores:
        explanation += f"\n(Recommendation personalized based on your usage patterns)"
    
    return CardRecommendation(
        card=best_card,
        reward_value=best_value,
        explanation=explanation
    ) 