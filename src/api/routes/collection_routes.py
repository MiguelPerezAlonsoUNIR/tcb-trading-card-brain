"""
Collection management API routes
Handles user card collection operations
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user

from ...services import CollectionService
from ...core.constants import API_MESSAGES
from ..utils import login_required_api
from structure_decks import get_structure_deck_cards

collection_bp = Blueprint('collection', __name__)


@collection_bp.route('/collection', methods=['GET', 'POST'])
@login_required_api
def manage_collection():
    """Get user's card collection or add cards"""
    if request.method == 'GET':
        # Get all cards in user's collection
        collection = CollectionService.get_user_collection(current_user.id)
        return jsonify({
            'success': True,
            'collection': collection
        })
    
    elif request.method == 'POST':
        # Add or update card in collection
        data = request.json
        card_name = data.get('card_name', '')
        quantity = data.get('quantity', 1)
        
        success, collection_item, error = CollectionService.add_or_update_card(
            current_user.id, card_name, quantity
        )
        
        if not success:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'collection_item': collection_item
        })


@collection_bp.route('/collection/<int:item_id>', methods=['DELETE'])
@login_required_api
def remove_from_collection(item_id):
    """Remove a card from user's collection"""
    success, error = CollectionService.remove_card(item_id, current_user.id)
    
    if not success:
        status_code = 404 if error == API_MESSAGES['COLLECTION_ITEM_NOT_FOUND'] else 500
        return jsonify({
            'success': False,
            'error': error
        }), status_code
    
    return jsonify({
        'success': True
    })


@collection_bp.route('/collection/add-structure-deck', methods=['POST'])
@login_required_api
def add_structure_deck_to_collection():
    """Add all cards from a structure deck to user's collection"""
    data = request.json
    deck_code = data.get('deck_code', '').strip().upper()
    
    if not deck_code:
        return jsonify({
            'success': False,
            'error': API_MESSAGES['DECK_CODE_REQUIRED']
        }), 400
    
    # Get structure deck cards
    deck_cards = get_structure_deck_cards(deck_code)
    if not deck_cards:
        return jsonify({
            'success': False,
            'error': f'{API_MESSAGES["STRUCTURE_DECK_NOT_FOUND"]}: {deck_code}'
        }), 404
    
    success, result, error = CollectionService.add_structure_deck(
        current_user.id, deck_cards
    )
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 500
    
    return jsonify({
        'success': True,
        'message': f'Successfully added structure deck {deck_code} to your collection',
        'deck_code': deck_code,
        **result
    })
