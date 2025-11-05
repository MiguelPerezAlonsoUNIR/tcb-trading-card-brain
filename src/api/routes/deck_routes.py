"""
Deck management API routes
Handles deck CRUD operations
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user

from ...services import DeckService
from ...core.constants import API_MESSAGES
from ..utils import login_required_api

deck_bp = Blueprint('decks', __name__)


@deck_bp.route('/decks', methods=['GET', 'POST'])
@login_required_api
def manage_decks():
    """Get all user decks or create a new deck"""
    if request.method == 'GET':
        # Get all decks for the current user
        decks = DeckService.get_user_decks(current_user.id)
        return jsonify({
            'success': True,
            'decks': decks
        })
    
    elif request.method == 'POST':
        # Create a new deck
        data = request.json
        name = data.get('name', '')
        strategy = data.get('strategy', 'balanced')
        color = data.get('color', 'any')
        leader = data.get('leader')
        main_deck = data.get('main_deck', [])
        
        success, deck, error = DeckService.create_deck(
            current_user.id, name, strategy, color, leader, main_deck
        )
        
        if not success:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        return jsonify({
            'success': True,
            'deck': deck.to_dict()
        })


@deck_bp.route('/decks/<int:deck_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required_api
def manage_single_deck(deck_id):
    """Get, update, or delete a specific deck"""
    deck = DeckService.get_deck_by_id(deck_id, current_user.id)
    
    if not deck:
        return jsonify({
            'success': False,
            'error': API_MESSAGES['DECK_NOT_FOUND']
        }), 404
    
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'deck': deck.to_dict()
        })
    
    elif request.method == 'PUT':
        # Update deck
        data = request.json
        
        success, error = DeckService.update_deck(
            deck,
            name=data.get('name'),
            strategy=data.get('strategy'),
            color=data.get('color'),
            leader=data.get('leader'),
            main_deck=data.get('main_deck')
        )
        
        if not success:
            return jsonify({
                'success': False,
                'error': error
            }), 500
        
        return jsonify({
            'success': True,
            'deck': deck.to_dict()
        })
    
    elif request.method == 'DELETE':
        # Delete deck
        success, error = DeckService.delete_deck(deck)
        
        if not success:
            return jsonify({
                'success': False,
                'error': error
            }), 500
        
        return jsonify({
            'success': True
        })
