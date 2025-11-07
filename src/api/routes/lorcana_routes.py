"""
Lorcana-specific API routes
Handles deck building, analysis, and Lorcana-specific operations
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user
import logging

from lorcana_deck_builder import LorcanaDeckBuilder
from ...services import CollectionService
from ...models import db
from ...core.constants import API_MESSAGES

lorcana_bp = Blueprint('lorcana', __name__)
logger = logging.getLogger(__name__)


@lorcana_bp.route('/cards', methods=['GET'])
def get_lorcana_cards():
    """Get all available Lorcana cards"""
    deck_builder = LorcanaDeckBuilder(db_session=db.session)
    return jsonify(deck_builder.get_all_cards())


@lorcana_bp.route('/build-deck', methods=['POST'])
def build_lorcana_deck():
    """Build a Lorcana deck based on user preferences"""
    data = request.json
    strategy = data.get('strategy', 'balanced')
    color = data.get('color', 'any')
    
    try:
        deck_builder = LorcanaDeckBuilder(db_session=db.session)
        deck = deck_builder.build_deck(strategy=strategy, color=color)
        return jsonify({
            'success': True,
            'deck': deck
        })
    except Exception as e:
        logger.error(f"Error building Lorcana deck: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to build deck'
        }), 400


@lorcana_bp.route('/analyze-deck', methods=['POST'])
def analyze_lorcana_deck():
    """Analyze a Lorcana deck and provide AI-powered suggestions"""
    data = request.json
    deck = data.get('deck', [])
    
    try:
        deck_builder = LorcanaDeckBuilder(db_session=db.session)
        analysis = deck_builder.analyze_deck(deck)
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        logger.error(f"Error analyzing Lorcana deck: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to analyze deck'
        }), 400


@lorcana_bp.route('/suggest-deck', methods=['POST'])
def suggest_lorcana_deck_from_collection():
    """Build a Lorcana deck based on user's collection (requires authentication)"""
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
        deck_builder = LorcanaDeckBuilder(db_session=db.session)
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
        logger.error(f"Error suggesting Lorcana deck: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to suggest deck'
        }), 400


@lorcana_bp.route('/suggest-improvements', methods=['POST'])
def suggest_lorcana_deck_improvements():
    """Suggest improvements for an existing Lorcana deck"""
    data = request.json
    deck = data.get('deck')
    
    if not deck:
        return jsonify({
            'success': False,
            'error': 'Deck required'
        }), 400
    
    # Validate deck structure
    if 'main_deck' not in deck:
        return jsonify({
            'success': False,
            'error': 'Invalid deck structure'
        }), 400
    
    try:
        # Get user's collection if authenticated
        owned_cards = {}
        if current_user.is_authenticated:
            owned_cards = CollectionService.get_collection_as_dict(current_user.id)
        
        # Generate improvement suggestions
        deck_builder = LorcanaDeckBuilder(db_session=db.session)
        improvements = deck_builder.suggest_improvements(deck, owned_cards)
        
        return jsonify({
            'success': True,
            'improvements': improvements
        })
    except Exception as e:
        logger.error(f"Error suggesting Lorcana improvements: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to suggest improvements'
        }), 400
