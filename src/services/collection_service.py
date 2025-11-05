"""
Collection service
Handles user card collection business logic
"""
from typing import List, Dict, Optional, Tuple

from ..models import db, UserCollection


class CollectionService:
    """Service for collection operations"""
    
    @staticmethod
    def get_user_collection(user_id: int) -> List[Dict]:
        """Get all cards in user's collection"""
        collection = UserCollection.query.filter_by(user_id=user_id).all()
        return [
            {
                'id': item.id,
                'card_name': item.card_name,
                'quantity': item.quantity,
                'added_at': item.added_at.isoformat() if item.added_at else None
            }
            for item in collection
        ]
    
    @staticmethod
    def get_collection_as_dict(user_id: int) -> Dict[str, int]:
        """Get collection as a dictionary of card_name -> quantity"""
        collection = UserCollection.query.filter_by(user_id=user_id).all()
        return {item.card_name: item.quantity for item in collection}
    
    @staticmethod
    def add_or_update_card(user_id: int, card_name: str, quantity: int) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Add or update a card in user's collection
        
        Returns:
            (success, collection_item_dict, error_message)
        """
        if not card_name or not card_name.strip():
            return False, None, 'Card name is required'
        
        try:
            card_name = card_name.strip()
            
            # Check if card already exists in collection
            collection_item = UserCollection.query.filter_by(
                user_id=user_id,
                card_name=card_name
            ).first()
            
            if collection_item:
                # Update quantity
                collection_item.quantity = quantity
            else:
                # Add new card
                collection_item = UserCollection(
                    user_id=user_id,
                    card_name=card_name,
                    quantity=quantity
                )
                db.session.add(collection_item)
            
            db.session.commit()
            
            return True, {
                'id': collection_item.id,
                'card_name': collection_item.card_name,
                'quantity': collection_item.quantity
            }, None
        except Exception as e:
            db.session.rollback()
            return False, None, f'Failed to update collection: {str(e)}'
    
    @staticmethod
    def remove_card(item_id: int, user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Remove a card from user's collection
        
        Returns:
            (success, error_message)
        """
        collection_item = UserCollection.query.filter_by(
            id=item_id,
            user_id=user_id
        ).first()
        
        if not collection_item:
            return False, 'Collection item not found'
        
        try:
            db.session.delete(collection_item)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f'Failed to remove from collection: {str(e)}'
    
    @staticmethod
    def add_structure_deck(user_id: int, deck_cards: Dict[str, int]) -> Tuple[bool, Dict, Optional[str]]:
        """
        Add all cards from a structure deck to user's collection
        
        Args:
            user_id: User ID
            deck_cards: Dictionary of card_name -> quantity
            
        Returns:
            (success, result_dict, error_message)
        """
        try:
            added_cards = []
            updated_cards = []
            
            for card_name, quantity in deck_cards.items():
                # Check if card already exists in collection
                collection_item = UserCollection.query.filter_by(
                    user_id=user_id,
                    card_name=card_name
                ).first()
                
                if collection_item:
                    # Update quantity (add to existing)
                    old_quantity = collection_item.quantity
                    collection_item.quantity += quantity
                    updated_cards.append({
                        'card_name': card_name,
                        'added_quantity': quantity,
                        'old_quantity': old_quantity,
                        'new_quantity': collection_item.quantity
                    })
                else:
                    # Add new card
                    collection_item = UserCollection(
                        user_id=user_id,
                        card_name=card_name,
                        quantity=quantity
                    )
                    db.session.add(collection_item)
                    added_cards.append({
                        'card_name': card_name,
                        'quantity': quantity
                    })
            
            db.session.commit()
            
            return True, {
                'added_cards': added_cards,
                'updated_cards': updated_cards,
                'total_cards_modified': len(added_cards) + len(updated_cards)
            }, None
        except Exception as e:
            db.session.rollback()
            return False, {}, f'Failed to add structure deck: {str(e)}'
