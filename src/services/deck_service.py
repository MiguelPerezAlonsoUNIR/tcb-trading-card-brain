"""
Deck service
Handles deck management business logic
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from ..models import db, Deck, User


class DeckService:
    """Service for deck operations"""
    
    @staticmethod
    def get_user_decks(user_id: int) -> List[Dict]:
        """Get all decks for a user"""
        decks = Deck.query.filter_by(user_id=user_id).order_by(Deck.updated_at.desc()).all()
        return [deck.to_dict() for deck in decks]
    
    @staticmethod
    def get_deck_by_id(deck_id: int, user_id: int) -> Optional[Deck]:
        """Get a specific deck by ID for a user"""
        return Deck.query.filter_by(id=deck_id, user_id=user_id).first()
    
    @staticmethod
    def create_deck(user_id: int, name: str, strategy: str, color: str,
                   leader: Dict, main_deck: List[Dict]) -> Tuple[bool, Optional[Deck], Optional[str]]:
        """
        Create a new deck
        
        Returns:
            (success, deck, error_message)
        """
        if not name or not name.strip():
            return False, None, 'Deck name is required'
        
        try:
            deck = Deck(
                user_id=user_id,
                name=name.strip(),
                strategy=strategy,
                color=color
            )
            deck.set_leader(leader)
            deck.set_main_deck(main_deck)
            
            db.session.add(deck)
            db.session.commit()
            
            return True, deck, None
        except Exception as e:
            db.session.rollback()
            return False, None, f'Failed to save deck: {str(e)}'
    
    @staticmethod
    def update_deck(deck: Deck, name: Optional[str] = None, strategy: Optional[str] = None,
                   color: Optional[str] = None, leader: Optional[Dict] = None,
                   main_deck: Optional[List[Dict]] = None) -> Tuple[bool, Optional[str]]:
        """
        Update an existing deck
        
        Returns:
            (success, error_message)
        """
        try:
            if name is not None:
                deck.name = name.strip()
            if strategy is not None:
                deck.strategy = strategy
            if color is not None:
                deck.color = color
            if leader is not None:
                deck.set_leader(leader)
            if main_deck is not None:
                deck.set_main_deck(main_deck)
            
            deck.updated_at = datetime.utcnow()
            db.session.commit()
            
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to update deck: {str(e)}'
    
    @staticmethod
    def delete_deck(deck: Deck) -> Tuple[bool, Optional[str]]:
        """
        Delete a deck
        
        Returns:
            (success, error_message)
        """
        try:
            db.session.delete(deck)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to delete deck: {str(e)}'
