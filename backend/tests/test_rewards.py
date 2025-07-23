import pytest
from app.models import Card, InputQuery, Category, RewardType
from app.rewards import calculate_reward_value, get_best_card

@pytest.fixture
def sample_card():
    return Card(
        id="test-card",
        name="Test Card",
        issuer="Test Bank",
        rewards={
            Category.DINING: 3.0,
            Category.TRAVEL: 2.0,
            Category.OTHER: 1.0
        },
        reward_type=RewardType.POINTS,
        annual_fee=0.0,
        foreign_transaction_fee=0.0
    )

def test_calculate_reward_value(sample_card):
    # Test regular purchase
    query = InputQuery(
        category=Category.DINING,
        amount=100.0,
        foreign_transaction=False
    )
    value = calculate_reward_value(sample_card, query)
    assert value == 3.0  # 3% of $100

    # Test foreign transaction
    query_foreign = InputQuery(
        category=Category.DINING,
        amount=100.0,
        foreign_transaction=True
    )
    value_foreign = calculate_reward_value(sample_card, query_foreign)
    assert value_foreign == 3.0  # 3% reward, 0% foreign transaction fee

def test_calculate_reward_value_with_foreign_fee():
    card_with_fee = Card(
        id="test-card-fee",
        name="Test Card with Fee",
        issuer="Test Bank",
        rewards={Category.DINING: 3.0},
        reward_type=RewardType.POINTS,
        annual_fee=0.0,
        foreign_transaction_fee=3.0
    )
    
    query = InputQuery(
        category=Category.DINING,
        amount=100.0,
        foreign_transaction=True
    )
    
    value = calculate_reward_value(card_with_fee, query)
    assert value == 0.0  # 3% reward - 3% foreign transaction fee 