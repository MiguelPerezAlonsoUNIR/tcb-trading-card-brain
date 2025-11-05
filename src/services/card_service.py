"""
Card service
Handles card database operations
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from ..models import db, Card, CardSet


class CardService:
    """Service for card database operations"""
    
    @staticmethod
    def get_all_cards(card_type: Optional[str] = None, 
                     color: Optional[str] = None,
                     set_code: Optional[str] = None) -> List[Dict]:
        """
        Get all cards with optional filtering
        
        Args:
            card_type: Filter by card type
            color: Filter by color
            set_code: Filter by set code
            
        Returns:
            List of card dictionaries
        """
        query = Card.query
        
        if card_type:
            query = query.filter_by(card_type=card_type)
        
        if color:
            # Filter by color (stored as JSON array)
            query = query.filter(Card.colors.like(f'%"{color}"%'))
        
        if set_code:
            card_set = CardSet.query.filter_by(code=set_code).first()
            if card_set:
                query = query.filter_by(set_id=card_set.id)
        
        cards = query.all()
        return [card.to_dict() for card in cards]
    
    @staticmethod
    def get_card_by_id(card_id: int) -> Optional[Card]:
        """Get a card by ID"""
        return Card.query.get(card_id)
    
    @staticmethod
    def create_card(name: str, card_type: str, colors: List[str], cost: int,
                   set_code: str, card_number: str, power: Optional[int] = None,
                   life: Optional[int] = None, attribute: Optional[str] = None,
                   effect: Optional[str] = None, rarity: Optional[str] = None,
                   image_url: Optional[str] = None,
                   set_name: Optional[str] = None) -> Tuple[bool, Optional[Card], Optional[str]]:
        """
        Create a new card
        
        Returns:
            (success, card, error_message)
        """
        # Get or create card set
        card_set = CardSet.query.filter_by(code=set_code).first()
        if not card_set:
            card_set = CardSet(
                code=set_code,
                name=set_name or f'Set {set_code}'
            )
            db.session.add(card_set)
            db.session.flush()
        
        # Check if card already exists
        existing_card = Card.query.filter_by(
            set_id=card_set.id,
            card_number=card_number
        ).first()
        
        if existing_card:
            return False, None, f'Card {set_code}-{card_number} already exists'
        
        try:
            card = Card(
                name=name,
                card_type=card_type,
                power=power,
                cost=cost,
                life=life,
                attribute=attribute,
                effect=effect,
                set_id=card_set.id,
                card_number=card_number,
                rarity=rarity,
                image_url=image_url
            )
            card.set_colors(colors)
            
            db.session.add(card)
            db.session.commit()
            
            return True, card, None
        except Exception as e:
            db.session.rollback()
            return False, None, f'Failed to add card: {str(e)}'
    
    @staticmethod
    def update_card(card: Card, **kwargs) -> Tuple[bool, Optional[str]]:
        """
        Update an existing card
        
        Returns:
            (success, error_message)
        """
        try:
            # Update fields if provided
            if 'name' in kwargs:
                card.name = kwargs['name']
            if 'type' in kwargs:
                card.card_type = kwargs['type']
            if 'colors' in kwargs:
                card.set_colors(kwargs['colors'])
            if 'power' in kwargs:
                card.power = kwargs['power']
            if 'cost' in kwargs:
                card.cost = kwargs['cost']
            if 'life' in kwargs:
                card.life = kwargs['life']
            if 'attribute' in kwargs:
                card.attribute = kwargs['attribute']
            if 'effect' in kwargs:
                card.effect = kwargs['effect']
            if 'rarity' in kwargs:
                card.rarity = kwargs['rarity']
            if 'image_url' in kwargs:
                card.image_url = kwargs['image_url']
            if 'card_number' in kwargs:
                card.card_number = kwargs['card_number']
            
            # Update set if provided
            if 'set' in kwargs:
                card_set = CardSet.query.filter_by(code=kwargs['set']).first()
                if card_set:
                    card.set_id = card_set.id
            
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to update card: {str(e)}'
    
    @staticmethod
    def delete_card(card: Card) -> Tuple[bool, Optional[str]]:
        """
        Delete a card
        
        Returns:
            (success, error_message)
        """
        try:
            db.session.delete(card)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to delete card: {str(e)}'
    
    @staticmethod
    def get_all_card_sets() -> List[Dict]:
        """Get all card sets"""
        card_sets = CardSet.query.all()
        return [cs.to_dict() for cs in card_sets]
    
    @staticmethod
    def create_card_set(code: str, name: str, 
                       release_date: Optional[datetime] = None) -> Tuple[bool, Optional[CardSet], Optional[str]]:
        """
        Create a new card set
        
        Returns:
            (success, card_set, error_message)
        """
        # Check if set already exists
        existing_set = CardSet.query.filter_by(code=code).first()
        if existing_set:
            return False, None, f'Card set {code} already exists'
        
        try:
            card_set = CardSet(
                code=code,
                name=name,
                release_date=release_date
            )
            
            db.session.add(card_set)
            db.session.commit()
            
            return True, card_set, None
        except Exception as e:
            db.session.rollback()
            return False, None, f'Failed to add card set: {str(e)}'
