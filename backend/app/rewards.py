from typing import List, Dict
from .models import Card, InputQuery, CardRecommendation, Category

def load_card_data() -> List[Card]:
    """
    Load card data from JSON file
    TODO: Implement actual loading from card_rewards.json
    """
    return []

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
    
    return reward_value

def get_best_card(query: InputQuery) -> CardRecommendation:
    """
    Determine the best card to use for a given purchase
    """
    cards = load_card_data()
    if not cards:
        raise ValueError("No cards available")

    best_card = None
    best_value = float('-inf')
    
    for card in cards:
        value = calculate_reward_value(card, query)
        if value > best_value:
            best_card = card
            best_value = value
    
    if not best_card:
        raise ValueError("Could not determine best card")
    
    explanation = (
        f"Using {best_card.name} will earn you "
        f"{best_value:.2f} {best_card.reward_type.value} "
        f"on your {query.amount:.2f} {query.category} purchase"
    )
    
    return CardRecommendation(
        card=best_card,
        reward_value=best_value,
        explanation=explanation
    ) 