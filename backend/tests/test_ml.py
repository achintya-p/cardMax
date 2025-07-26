import pytest
from ..app.ml_models import CategoryPredictor, PersonalizedRecommender
from ..app.models import Category, Card, RewardType

def test_category_predictor():
    predictor = CategoryPredictor()
    
    # Test training
    descriptions = [
        "UBER EATS DELIVERY",
        "AMAZON.COM",
        "SHELL GAS STATION",
        "WALMART GROCERY"
    ]
    categories = [
        Category.DINING,
        Category.ONLINE_SHOPPING,
        Category.GAS,
        Category.GROCERIES
    ]
    
    predictor.train(descriptions, categories)
    assert predictor.is_trained
    
    # Test prediction
    pred = predictor.predict("DOORDASH FOOD DELIVERY")
    assert pred == Category.DINING
    
    pred = predictor.predict("EXXON GAS")
    assert pred == Category.GAS

def test_personalized_recommender():
    recommender = PersonalizedRecommender()
    
    # Test card scoring
    user_id = "test_user"
    cards = [
        Card(
            id="card1",
            name="Test Card 1",
            issuer="Test Bank",
            rewards={
                Category.DINING: 3.0,
                Category.OTHER: 1.0
            },
            reward_type=RewardType.POINTS
        ),
        Card(
            id="card2",
            name="Test Card 2",
            issuer="Test Bank",
            rewards={
                Category.GAS: 4.0,
                Category.OTHER: 1.0
            },
            reward_type=RewardType.CASHBACK
        )
    ]
    
    # Get initial scores
    scores = recommender.get_personalized_scores(user_id, cards)
    assert len(scores) == 2
    
    # Update embeddings
    recommender.update_embeddings(user_id, "card1", 1.0)
    
    # Get updated scores
    new_scores = recommender.get_personalized_scores(user_id, cards)
    assert len(new_scores) == 2
    
    # Score for card1 should be higher after positive interaction
    assert new_scores["card1"] > scores["card1"] 