"""
Game-related API routes
Handles deck building, analysis, combat simulation, and structure decks
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user
import logging

from deck_builder import OnePieceDeckBuilder
from combat_simulator import CombatSimulator
from structure_decks import get_all_structure_decks, get_structure_deck
from ...services import CollectionService
from ...models import db
from ...core.constants import API_MESSAGES

game_bp = Blueprint('game', __name__)
logger = logging.getLogger(__name__)

# Initialize game components
combat_simulator = CombatSimulator()


@game_bp.route('/cards', methods=['GET'])
def get_cards():
    """Get all available One Piece TCG cards"""
    deck_builder = OnePieceDeckBuilder(db_session=db.session)
    return jsonify(deck_builder.get_all_cards())


@game_bp.route('/build-deck', methods=['POST'])
def build_deck():
    """Build a deck based on user preferences"""
    data = request.json
    strategy = data.get('strategy', 'balanced')
    color = data.get('color', 'any')
    leader = data.get('leader', None)
    
    try:
        deck_builder = OnePieceDeckBuilder(db_session=db.session)
        deck = deck_builder.build_deck(strategy=strategy, color=color, leader=leader)
        return jsonify({
            'success': True,
            'deck': deck
        })
    except Exception as e:
        logger.error(f"Error building deck: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': API_MESSAGES['BUILD_DECK_FAILED']
        }), 400


@game_bp.route('/analyze-deck', methods=['POST'])
def analyze_deck():
    """Analyze a deck and provide AI-powered suggestions"""
    data = request.json
    deck = data.get('deck', [])
    
    try:
        deck_builder = OnePieceDeckBuilder(db_session=db.session)
        analysis = deck_builder.analyze_deck(deck)
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        logger.error(f"Error analyzing deck: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': API_MESSAGES['ANALYZE_DECK_FAILED']
        }), 400


@game_bp.route('/suggest-deck', methods=['POST'])
def suggest_deck_from_collection():
    """Build a deck based on user's collection (requires authentication)"""
    if not current_user.is_authenticated:
        return jsonify({
            'success': False,
            'error': API_MESSAGES['AUTH_REQUIRED']
        }), 401
    
    data = request.json
    strategy = data.get('strategy', 'balanced')
    color = data.get('color', 'any')
    
    # Get user's collection
    owned_cards = CollectionService.get_collection_as_dict(current_user.id)
    
    try:
        # Build deck with collection awareness
        deck_builder = OnePieceDeckBuilder(db_session=db.session)
        deck = deck_builder.build_deck_from_collection(
            strategy=strategy,
            color=color,
            owned_cards=owned_cards
        )
        return jsonify({
            'success': True,
            'deck': deck
        })
    except Exception as e:
        logger.error(f"Error suggesting deck: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': API_MESSAGES['SUGGEST_DECK_FAILED']
        }), 400


@game_bp.route('/suggest-improvements', methods=['POST'])
def suggest_deck_improvements():
    """Suggest improvements for an existing deck"""
    data = request.json
    deck = data.get('deck')
    
    if not deck:
        return jsonify({
            'success': False,
            'error': API_MESSAGES['DECK_REQUIRED']
        }), 400
    
    # Validate deck structure
    if 'leader' not in deck or 'main_deck' not in deck:
        return jsonify({
            'success': False,
            'error': API_MESSAGES['DECK_STRUCTURE_INVALID']
        }), 400
    
    try:
        # Get user's collection if authenticated
        owned_cards = {}
        if current_user.is_authenticated:
            owned_cards = CollectionService.get_collection_as_dict(current_user.id)
        
        # Generate improvement suggestions
        deck_builder = OnePieceDeckBuilder(db_session=db.session)
        improvements = deck_builder.suggest_improvements(deck, owned_cards)
        
        return jsonify({
            'success': True,
            'improvements': improvements
        })
    except Exception as e:
        logger.error(f"Error suggesting improvements: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': API_MESSAGES['IMPROVEMENTS_FAILED']
        }), 400


@game_bp.route('/structure-decks', methods=['GET'])
def get_structure_decks_list():
    """Get list of all available structure decks"""
    try:
        decks = get_all_structure_decks()
        # Return simplified info without full card lists
        deck_list = [{
            'code': deck['code'],
            'name': deck['name'],
            'description': deck['description'],
            'color': deck['color'],
            'leader': deck['leader']
        } for deck in decks]
        return jsonify({
            'success': True,
            'decks': deck_list
        })
    except Exception as e:
        logger.error(f"Error getting structure decks: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to get structure decks'
        }), 500


@game_bp.route('/structure-decks/<deck_code>', methods=['GET'])
def get_structure_deck_details(deck_code):
    """Get details of a specific structure deck including card list"""
    try:
        deck = get_structure_deck(deck_code)
        if not deck:
            return jsonify({
                'success': False,
                'error': API_MESSAGES['STRUCTURE_DECK_NOT_FOUND']
            }), 404
        
        return jsonify({
            'success': True,
            'deck': deck
        })
    except Exception as e:
        logger.error(f"Error getting structure deck: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to get structure deck'
        }), 500


@game_bp.route('/opponent-decks', methods=['GET'])
def get_opponent_decks():
    """Get list of available opponent decks for simulation"""
    try:
        opponent_decks = combat_simulator.get_available_opponent_decks()
        return jsonify({
            'success': True,
            'decks': opponent_decks
        })
    except Exception as e:
        logger.error(f"Error getting opponent decks: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to load opponent decks'
        }), 500


@game_bp.route('/simulate-combat', methods=['POST'])
def simulate_combat():
    """Simulate combat between player's deck and an opponent deck"""
    data = request.json
    player_deck = data.get('player_deck')
    opponent_deck_id = data.get('opponent_deck_id')
    num_simulations = data.get('num_simulations', 1000)
    
    if not player_deck:
        return jsonify({
            'success': False,
            'error': API_MESSAGES['PLAYER_DECK_REQUIRED']
        }), 400
    
    if not opponent_deck_id:
        return jsonify({
            'success': False,
            'error': API_MESSAGES['OPPONENT_DECK_REQUIRED']
        }), 400
    
    try:
        # Build opponent deck based on selection
        opponent_decks_info = combat_simulator.get_available_opponent_decks()
        opponent_info = next((d for d in opponent_decks_info if d['id'] == opponent_deck_id), None)
        
        if not opponent_info:
            return jsonify({
                'success': False,
                'error': API_MESSAGES['INVALID_OPPONENT_DECK']
            }), 400
        
        # Build the actual opponent deck
        deck_builder = OnePieceDeckBuilder(db_session=db.session)
        opponent_deck = deck_builder.build_deck(
            strategy=opponent_info['strategy'],
            color=opponent_info['color']
        )
        
        # Run simulation
        results = combat_simulator.simulate_combat(
            player_deck,
            opponent_deck,
            num_simulations=num_simulations
        )
        
        # Add opponent info to results
        results['opponent_name'] = opponent_info['name']
        results['opponent_description'] = opponent_info['description']
        results['opponent_tournament_win_rate'] = opponent_info['win_rate']
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        logger.error(f"Error simulating combat: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': API_MESSAGES['COMBAT_SIMULATION_FAILED']
        }), 400
