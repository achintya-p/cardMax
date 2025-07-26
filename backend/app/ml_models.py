from typing import List, Dict, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path
import pandas as pd
from .models import Category, Card, UserWallet

class CategoryPredictor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.classifier = MultinomialNB()
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
    def train(self, descriptions: List[str], categories: List[Category]):
        """Train the category predictor model"""
        X = self.vectorizer.fit_transform(descriptions)
        y = self.label_encoder.fit_transform(categories)
        self.classifier.fit(X, y)
        self.is_trained = True
        
    def predict(self, description: str) -> Category:
        """Predict category from transaction description"""
        if not self.is_trained:
            return Category.OTHER
            
        X = self.vectorizer.transform([description])
        y_pred = self.classifier.predict(X)
        category = self.label_encoder.inverse_transform(y_pred)[0]
        return Category(category)
        
    def save(self, path: str = "models/category_predictor.joblib"):
        """Save the model to disk"""
        model_path = Path(path)
        model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({
            'vectorizer': self.vectorizer,
            'classifier': self.classifier,
            'label_encoder': self.label_encoder,
            'is_trained': self.is_trained
        }, path)
        
    def load(self, path: str = "models/category_predictor.joblib"):
        """Load the model from disk"""
        if not Path(path).exists():
            return
            
        model_dict = joblib.load(path)
        self.vectorizer = model_dict['vectorizer']
        self.classifier = model_dict['classifier']
        self.label_encoder = model_dict['label_encoder']
        self.is_trained = model_dict['is_trained']

class PersonalizedRecommender:
    def __init__(self):
        self.user_embeddings = {}
        self.card_embeddings = {}
        self.embedding_size = 32
        
    def _initialize_embeddings(self, user_id: str, cards: List[Card]):
        """Initialize embeddings for new users and cards"""
        if user_id not in self.user_embeddings:
            self.user_embeddings[user_id] = np.random.normal(0, 0.1, self.embedding_size)
            
        for card in cards:
            if card.id not in self.card_embeddings:
                self.card_embeddings[card.id] = np.random.normal(0, 0.1, self.embedding_size)
                
    def update_embeddings(self, user_id: str, card_id: str, reward_value: float):
        """Update embeddings based on user-card interactions"""
        learning_rate = 0.01
        user_embed = self.user_embeddings[user_id]
        card_embed = self.card_embeddings[card_id]
        
        # Simple gradient update
        pred = np.dot(user_embed, card_embed)
        error = reward_value - pred
        
        self.user_embeddings[user_id] += learning_rate * error * card_embed
        self.card_embeddings[card_id] += learning_rate * error * user_embed
        
    def get_personalized_scores(self, user_id: str, cards: List[Card]) -> Dict[str, float]:
        """Get personalized scores for each card"""
        self._initialize_embeddings(user_id, cards)
        
        scores = {}
        user_embed = self.user_embeddings[user_id]
        
        for card in cards:
            card_embed = self.card_embeddings[card.id]
            scores[card.id] = float(np.dot(user_embed, card_embed))
            
        return scores
        
    def save(self, path: str = "models/recommender.joblib"):
        """Save the model to disk"""
        model_path = Path(path)
        model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({
            'user_embeddings': self.user_embeddings,
            'card_embeddings': self.card_embeddings,
            'embedding_size': self.embedding_size
        }, path)
        
    def load(self, path: str = "models/recommender.joblib"):
        """Load the model from disk"""
        if not Path(path).exists():
            return
            
        model_dict = joblib.load(path)
        self.user_embeddings = model_dict['user_embeddings']
        self.card_embeddings = model_dict['card_embeddings']
        self.embedding_size = model_dict['embedding_size']

# Global instances
category_predictor = CategoryPredictor()
recommender = PersonalizedRecommender()

# Try to load pre-trained models
try:
    category_predictor.load()
    recommender.load()
except Exception:
    pass  # Models will be trained as data becomes available 