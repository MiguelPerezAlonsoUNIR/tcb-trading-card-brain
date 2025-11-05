"""
Application constants
Centralizes all magic values and constants
"""

# Card types
CARD_TYPES = ['Leader', 'Character', 'Event', 'Stage']

# Card colors
COLORS = ['Red', 'Blue', 'Green', 'Purple', 'Black', 'Yellow']

# Deck strategies
STRATEGIES = ['aggressive', 'balanced', 'control']

# Card rarities
RARITIES = ['Common', 'Uncommon', 'Rare', 'Super Rare', 'Secret Rare', 'Leader']

# Authentication constraints
MIN_USERNAME_LENGTH = 3
MIN_PASSWORD_LENGTH = 6


def get_auth_error_message(error_type: str) -> str:
    """Get authentication error messages with dynamic values"""
    messages = {
        'USERNAME_TOO_SHORT': f'Username must be at least {MIN_USERNAME_LENGTH} characters',
        'PASSWORD_TOO_SHORT': f'Password must be at least {MIN_PASSWORD_LENGTH} characters',
    }
    return messages.get(error_type, '')

# Deck building strategies configuration
STRATEGY_CONFIG = {
    'aggressive': {
        'character_ratio': 0.75,
        'event_ratio': 0.20,
        'stage_ratio': 0.05,
        'preferred_cost_range': (1, 4),
        'avg_cost_target': 3.2
    },
    'balanced': {
        'character_ratio': 0.65,
        'event_ratio': 0.30,
        'stage_ratio': 0.05,
        'preferred_cost_range': (2, 6),
        'avg_cost_target': 4.2
    },
    'control': {
        'character_ratio': 0.55,
        'event_ratio': 0.35,
        'stage_ratio': 0.10,
        'preferred_cost_range': (4, 8),
        'avg_cost_target': 5.5
    }
}

# Combat simulation
CHARACTER_ATTACK_LEADER_CHANCE = 0.7
DEFAULT_SIMULATIONS = 1000

# API Response messages
API_MESSAGES = {
    'AUTH_REQUIRED': 'Authentication required',
    'INVALID_CREDENTIALS': 'Invalid username or password',
    'USERNAME_EXISTS': 'Username already exists',
    'USERNAME_REQUIRED': 'Username and password are required',
    'USERNAME_TOO_SHORT': 'Username is too short',
    'PASSWORD_TOO_SHORT': 'Password is too short',
    'DECK_NAME_REQUIRED': 'Deck name is required',
    'DECK_NOT_FOUND': 'Deck not found',
    'CARD_NAME_REQUIRED': 'Card name is required',
    'COLLECTION_ITEM_NOT_FOUND': 'Collection item not found',
    'DECK_CODE_REQUIRED': 'Deck code is required',
    'STRUCTURE_DECK_NOT_FOUND': 'Structure deck not found',
    'PLAYER_DECK_REQUIRED': 'Player deck is required',
    'OPPONENT_DECK_REQUIRED': 'Opponent deck selection is required',
    'INVALID_OPPONENT_DECK': 'Invalid opponent deck selection',
    'DECK_REQUIRED': 'Deck is required',
    'DECK_STRUCTURE_INVALID': 'Deck must include leader and main_deck',
    'BUILD_DECK_FAILED': 'Failed to build deck. Please try again.',
    'ANALYZE_DECK_FAILED': 'Failed to analyze deck. Please try again.',
    'SUGGEST_DECK_FAILED': 'Failed to suggest deck. Please try again.',
    'IMPROVEMENTS_FAILED': 'Failed to generate improvement suggestions. Please try again.',
    'COMBAT_SIMULATION_FAILED': 'Failed to simulate combat. Please try again.',
}
