"""
Card database API routes
Handles card database operations and admin endpoints
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import logging

from ...services import CardService
from ..utils import safe_error_response

logger = logging.getLogger(__name__)

card_bp = Blueprint('cards', __name__)


@card_bp.route('/admin/cards', methods=['GET'])
def list_all_cards():
    """List all cards with filtering options (admin endpoint)"""
    card_type = request.args.get('type')
    color = request.args.get('color')
    set_code = request.args.get('set')
    
    cards = CardService.get_all_cards(card_type, color, set_code)
    
    return jsonify({
        'success': True,
        'cards': cards,
        'count': len(cards)
    })


@card_bp.route('/admin/cards', methods=['POST'])
def add_card():
    """Add a new card to the database (admin endpoint)"""
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'type', 'colors', 'cost', 'set', 'card_number']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Missing required field: {field}'
            }), 400
    
    success, card, error = CardService.create_card(
        name=data['name'],
        card_type=data['type'],
        colors=data['colors'],
        cost=data['cost'],
        set_code=data['set'],
        card_number=data['card_number'],
        power=data.get('power'),
        life=data.get('life'),
        attribute=data.get('attribute'),
        effect=data.get('effect'),
        rarity=data.get('rarity'),
        image_url=data.get('image_url'),
        set_name=data.get('set_name')
    )
    
    if not success:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    return jsonify({
        'success': True,
        'card': card.to_dict(),
        'message': 'Card added successfully'
    }), 201


@card_bp.route('/admin/cards/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    """Update an existing card (admin endpoint)"""
    card = CardService.get_card_by_id(card_id)
    if not card:
        return jsonify({
            'success': False,
            'error': 'Card not found'
        }), 404
    
    data = request.json
    success, error = CardService.update_card(card, **data)
    
    if not success:
        return safe_error_response(
            error,
            'Failed to update card. Please try again.',
            500,
            f"Card update error for card {card_id}"
        )
    
    return jsonify({
        'success': True,
        'card': card.to_dict(),
        'message': 'Card updated successfully'
    })


@card_bp.route('/admin/cards/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    """Delete a card (admin endpoint)"""
    card = CardService.get_card_by_id(card_id)
    if not card:
        return jsonify({
            'success': False,
            'error': 'Card not found'
        }), 404
    
    card_name = card.name
    success, error = CardService.delete_card(card)
    
    if not success:
        return safe_error_response(
            error,
            'Failed to delete card. Please try again.',
            500,
            f"Card deletion error for card {card_id}"
        )
    
    return jsonify({
        'success': True,
        'message': f'Card "{card_name}" deleted successfully'
    })


@card_bp.route('/admin/card-sets', methods=['GET'])
def list_card_sets():
    """List all card sets (admin endpoint)"""
    card_sets = CardService.get_all_card_sets()
    
    return jsonify({
        'success': True,
        'card_sets': card_sets,
        'count': len(card_sets)
    })


@card_bp.route('/admin/card-sets', methods=['POST'])
def add_card_set():
    """Add a new card set (admin endpoint)"""
    data = request.json
    
    if 'code' not in data or 'name' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing required fields: code and name'
        }), 400
    
    release_date = None
    if 'release_date' in data:
        try:
            release_date = datetime.fromisoformat(data['release_date'])
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid release_date format. Use ISO format (YYYY-MM-DD)'
            }), 400
    
    success, card_set, error = CardService.create_card_set(
        data['code'], data['name'], release_date
    )
    
    if not success:
        status_code = 500 if 'Failed to add card set:' in str(error) else 400
        return safe_error_response(
            error,
            'Failed to add card set. Please try again.',
            status_code,
            "Card set creation error"
        )
    
    return jsonify({
        'success': True,
        'card_set': card_set.to_dict(),
        'message': 'Card set added successfully'
    }), 201
