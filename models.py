"""
Database models for user authentication and deck management
Backwards compatibility wrapper for new models module
"""
from src.models import db, User, Deck, UserCollection, CardSet, Card

# Export all models for backwards compatibility
__all__ = ['db', 'User', 'Deck', 'UserCollection', 'CardSet', 'Card']

# Models are now imported from src.models
# This file is kept for backwards compatibility
