"""
One Piece TCG Deck Builder Web Application
Uses AI to help build optimal decks for One Piece Trading Card Game
"""
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user
import json
import os
import logging
from deck_builder import OnePieceDeckBuilder
from models import db, User, Deck, UserCollection
from auth import hash_password, verify_password, login_required_api
from combat_simulator import CombatSimulator
from structure_decks import get_all_structure_decks, get_structure_deck, get_structure_deck_cards

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tcb.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the deck builder and combat simulator
deck_builder = OnePieceDeckBuilder()
combat_simulator = CombatSimulator()

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({
            'success': False,
            'error': 'Username and password are required'
        }), 400
    
    if len(username) < 3:
        return jsonify({
            'success': False,
            'error': 'Username must be at least 3 characters'
        }), 400
    
    if len(password) < 6:
        return jsonify({
            'success': False,
            'error': 'Password must be at least 6 characters'
        }), 400
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({
            'success': False,
            'error': 'Username already exists'
        }), 400
    
    try:
        # Create new user
        user = User(
            username=username,
            password_hash=hash_password(password)
        )
        db.session.add(user)
        db.session.commit()
        
        # Log the user in
        login_user(user)
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username
            }
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error registering user: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to register user'
        }), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Login a user"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({
            'success': False,
            'error': 'Username and password are required'
        }), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not verify_password(password, user.password_hash):
        return jsonify({
            'success': False,
            'error': 'Invalid username or password'
        }), 401
    
    login_user(user)
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username
        }
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout the current user"""
    logout_user()
    return jsonify({
        'success': True
    })

@app.route('/api/current-user', methods=['GET'])
def get_current_user():
    """Get the current logged-in user"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username
            }
        })
    return jsonify({
        'authenticated': False
    })

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

@app.route('/api/decks', methods=['GET', 'POST'])
@login_required_api
def manage_decks():
    """Get all user decks or create a new deck"""
    if request.method == 'GET':
        # Get all decks for the current user
        decks = Deck.query.filter_by(user_id=current_user.id).order_by(Deck.updated_at.desc()).all()
        return jsonify({
            'success': True,
            'decks': [deck.to_dict() for deck in decks]
        })
    
    elif request.method == 'POST':
        # Create a new deck
        data = request.json
        name = data.get('name', '').strip()
        strategy = data.get('strategy', 'balanced')
        color = data.get('color', 'any')
        leader = data.get('leader')
        main_deck = data.get('main_deck', [])
        
        if not name:
            return jsonify({
                'success': False,
                'error': 'Deck name is required'
            }), 400
        
        try:
            deck = Deck(
                user_id=current_user.id,
                name=name,
                strategy=strategy,
                color=color
            )
            deck.set_leader(leader)
            deck.set_main_deck(main_deck)
            
            db.session.add(deck)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'deck': deck.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving deck: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': 'Failed to save deck'
            }), 500

@app.route('/api/decks/<int:deck_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required_api
def manage_single_deck(deck_id):
    """Get, update, or delete a specific deck"""
    deck = Deck.query.filter_by(id=deck_id, user_id=current_user.id).first()
    
    if not deck:
        return jsonify({
            'success': False,
            'error': 'Deck not found'
        }), 404
    
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'deck': deck.to_dict()
        })
    
    elif request.method == 'PUT':
        # Update deck
        data = request.json
        
        if 'name' in data:
            deck.name = data['name'].strip()
        if 'strategy' in data:
            deck.strategy = data['strategy']
        if 'color' in data:
            deck.color = data['color']
        if 'leader' in data:
            deck.set_leader(data['leader'])
        if 'main_deck' in data:
            deck.set_main_deck(data['main_deck'])
        
        try:
            db.session.commit()
            return jsonify({
                'success': True,
                'deck': deck.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating deck: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': 'Failed to update deck'
            }), 500
    
    elif request.method == 'DELETE':
        # Delete deck
        try:
            db.session.delete(deck)
            db.session.commit()
            return jsonify({
                'success': True
            })
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting deck: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': 'Failed to delete deck'
            }), 500

@app.route('/api/collection', methods=['GET', 'POST'])
@login_required_api
def manage_collection():
    """Get user's card collection or add cards"""
    if request.method == 'GET':
        # Get all cards in user's collection
        collection = UserCollection.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'success': True,
            'collection': [
                {
                    'id': item.id,
                    'card_name': item.card_name,
                    'quantity': item.quantity,
                    'added_at': item.added_at.isoformat() if item.added_at else None
                }
                for item in collection
            ]
        })
    
    elif request.method == 'POST':
        # Add or update card in collection
        data = request.json
        card_name = data.get('card_name', '').strip()
        quantity = data.get('quantity', 1)
        
        if not card_name:
            return jsonify({
                'success': False,
                'error': 'Card name is required'
            }), 400
        
        try:
            # Check if card already exists in collection
            collection_item = UserCollection.query.filter_by(
                user_id=current_user.id,
                card_name=card_name
            ).first()
            
            if collection_item:
                # Update quantity
                collection_item.quantity = quantity
            else:
                # Add new card
                collection_item = UserCollection(
                    user_id=current_user.id,
                    card_name=card_name,
                    quantity=quantity
                )
                db.session.add(collection_item)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'collection_item': {
                    'id': collection_item.id,
                    'card_name': collection_item.card_name,
                    'quantity': collection_item.quantity
                }
            })
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating collection: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': 'Failed to update collection'
            }), 500

@app.route('/api/collection/<int:item_id>', methods=['DELETE'])
@login_required_api
def remove_from_collection(item_id):
    """Remove a card from user's collection"""
    collection_item = UserCollection.query.filter_by(
        id=item_id,
        user_id=current_user.id
    ).first()
    
    if not collection_item:
        return jsonify({
            'success': False,
            'error': 'Collection item not found'
        }), 404
    
    try:
        db.session.delete(collection_item)
        db.session.commit()
        return jsonify({
            'success': True
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error removing from collection: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to remove from collection'
        }), 500

@app.route('/api/suggest-deck', methods=['POST'])
@login_required_api
def suggest_deck_from_collection():
    """Build a deck based on user's collection"""
    data = request.json
    strategy = data.get('strategy', 'balanced')
    color = data.get('color', 'any')
    
    # Get user's collection
    collection = UserCollection.query.filter_by(user_id=current_user.id).all()
    owned_cards = {item.card_name: item.quantity for item in collection}
    
    try:
        # Build deck with collection awareness
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
            'error': 'Failed to suggest deck. Please try again.'
        }), 400

@app.route('/api/structure-decks', methods=['GET'])
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

@app.route('/api/structure-decks/<deck_code>', methods=['GET'])
def get_structure_deck_details(deck_code):
    """Get details of a specific structure deck including card list"""
    try:
        deck = get_structure_deck(deck_code)
        if not deck:
            return jsonify({
                'success': False,
                'error': 'Structure deck not found'
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

@app.route('/api/collection/add-structure-deck', methods=['POST'])
@login_required_api
def add_structure_deck_to_collection():
    """Add all cards from a structure deck to user's collection"""
    data = request.json
    deck_code = data.get('deck_code', '').strip().upper()
    
    if not deck_code:
        return jsonify({
            'success': False,
            'error': 'Deck code is required'
        }), 400
    
    # Get structure deck
    deck_cards = get_structure_deck_cards(deck_code)
    if not deck_cards:
        return jsonify({
            'success': False,
            'error': f'Structure deck {deck_code} not found'
        }), 404
    
    try:
        added_cards = []
        updated_cards = []
        
        # Add each card from the structure deck to the collection
        for card_name, quantity in deck_cards.items():
            # Check if card already exists in collection
            collection_item = UserCollection.query.filter_by(
                user_id=current_user.id,
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
                    user_id=current_user.id,
                    card_name=card_name,
                    quantity=quantity
                )
                db.session.add(collection_item)
                added_cards.append({
                    'card_name': card_name,
                    'quantity': quantity
                })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Successfully added structure deck {deck_code} to your collection',
            'deck_code': deck_code,
            'added_cards': added_cards,
            'updated_cards': updated_cards,
            'total_cards_modified': len(added_cards) + len(updated_cards)
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding structure deck to collection: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to add structure deck to collection'
        }), 500

@app.route('/api/opponent-decks', methods=['GET'])
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

@app.route('/api/simulate-combat', methods=['POST'])
def simulate_combat():
    """Simulate combat between player's deck and an opponent deck"""
    data = request.json
    player_deck = data.get('player_deck')
    opponent_deck_id = data.get('opponent_deck_id')
    num_simulations = data.get('num_simulations', 1000)
    
    if not player_deck:
        return jsonify({
            'success': False,
            'error': 'Player deck is required'
        }), 400
    
    if not opponent_deck_id:
        return jsonify({
            'success': False,
            'error': 'Opponent deck selection is required'
        }), 400
    
    try:
        # Build opponent deck based on selection
        opponent_decks_info = combat_simulator.get_available_opponent_decks()
        opponent_info = next((d for d in opponent_decks_info if d['id'] == opponent_deck_id), None)
        
        if not opponent_info:
            return jsonify({
                'success': False,
                'error': 'Invalid opponent deck selection'
            }), 400
        
        # Build the actual opponent deck
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
            'error': 'Failed to simulate combat. Please try again.'
        }), 400

@app.route('/api/suggest-improvements', methods=['POST'])
def suggest_deck_improvements():
    """Suggest improvements for an existing deck"""
    data = request.json
    deck = data.get('deck')
    
    if not deck:
        return jsonify({
            'success': False,
            'error': 'Deck is required'
        }), 400
    
    # Validate deck structure
    if 'leader' not in deck or 'main_deck' not in deck:
        return jsonify({
            'success': False,
            'error': 'Deck must include leader and main_deck'
        }), 400
    
    try:
        # Get user's collection if authenticated
        owned_cards = {}
        if current_user.is_authenticated:
            collection = UserCollection.query.filter_by(user_id=current_user.id).all()
            owned_cards = {item.card_name: item.quantity for item in collection}
        
        # Generate improvement suggestions
        improvements = deck_builder.suggest_improvements(deck, owned_cards)
        
        return jsonify({
            'success': True,
            'improvements': improvements
        })
    except Exception as e:
        logger.error(f"Error suggesting improvements: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to generate improvement suggestions. Please try again.'
        }), 400

if __name__ == '__main__':
    # Only enable debug mode in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
