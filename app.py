"""
One Piece TCG Deck Builder Web Application
Uses AI to help build optimal decks for One Piece Trading Card Game
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
import logging
from deck_builder import OnePieceDeckBuilder

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the deck builder
deck_builder = OnePieceDeckBuilder()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/cards', methods=['GET'])
def get_cards():
    """Get all available One Piece TCG cards"""
    return jsonify(deck_builder.get_all_cards())

@app.route('/api/build-deck', methods=['POST'])
def build_deck():
    """Build a deck based on user preferences"""
    data = request.json
    strategy = data.get('strategy', 'balanced')
    color = data.get('color', 'any')
    leader = data.get('leader', None)
    
    try:
        deck = deck_builder.build_deck(strategy=strategy, color=color, leader=leader)
        return jsonify({
            'success': True,
            'deck': deck
        })
    except Exception as e:
        logger.error(f"Error building deck: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to build deck. Please try again.'
        }), 400

@app.route('/api/analyze-deck', methods=['POST'])
def analyze_deck():
    """Analyze a deck and provide AI-powered suggestions"""
    data = request.json
    deck = data.get('deck', [])
    
    try:
        analysis = deck_builder.analyze_deck(deck)
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        logger.error(f"Error analyzing deck: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to analyze deck. Please try again.'
        }), 400

if __name__ == '__main__':
    # Only enable debug mode in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
