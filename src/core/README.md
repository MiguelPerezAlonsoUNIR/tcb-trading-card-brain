# Core (src/core/)

This directory contains core utilities, constants, and shared functionality used throughout the application.

## Core Files

### constants.py
Application-wide constants and configuration values.

**Constant Categories:**
- Card types (Leader, Character, Event, Stage)
- Colors (Red, Blue, Green, Purple, Black, Yellow)
- Strategies (Aggressive, Balanced, Control)
- Deck building parameters
- API messages and error codes

## Constants Overview

### Card Types
```python
CARD_TYPES = {
    'LEADER': 'Leader',
    'CHARACTER': 'Character',
    'EVENT': 'Event',
    'STAGE': 'Stage'
}
```

Used for validating and filtering cards by type.

### Card Colors
```python
COLORS = [
    'Red',
    'Blue',
    'Green',
    'Purple',
    'Black',
    'Yellow'
]
```

Valid colors for One Piece TCG cards and decks.

### Deck Building Strategies
```python
STRATEGIES = {
    'AGGRESSIVE': {
        'name': 'aggressive',
        'character_ratio': 0.70,
        'event_ratio': 0.30,
        'stage_ratio': 0.00,
        'avg_cost_target': 3.5,
        'low_cost_preference': True
    },
    'BALANCED': {
        'name': 'balanced',
        'character_ratio': 0.65,
        'event_ratio': 0.30,
        'stage_ratio': 0.05,
        'avg_cost_target': 4.5,
        'low_cost_preference': False
    },
    'CONTROL': {
        'name': 'control',
        'character_ratio': 0.60,
        'event_ratio': 0.40,
        'stage_ratio': 0.00,
        'avg_cost_target': 5.0,
        'low_cost_preference': False
    }
}
```

Strategy definitions with card distribution and cost preferences.

### Deck Rules
```python
DECK_SIZE = 50  # Main deck size
MAX_CARD_COPIES = 4  # Maximum copies per card (excluding leader)
MIN_USERNAME_LENGTH = 3
MIN_PASSWORD_LENGTH = 6
```

One Piece TCG official rules and application constraints.

### API Messages
```python
MESSAGES = {
    'SUCCESS': {
        'USER_REGISTERED': 'User registered successfully',
        'USER_LOGGED_IN': 'Logged in successfully',
        'DECK_SAVED': 'Deck saved successfully',
        # ... more success messages
    },
    'ERROR': {
        'INVALID_CREDENTIALS': 'Invalid username or password',
        'USERNAME_TAKEN': 'Username already taken',
        'DECK_NOT_FOUND': 'Deck not found',
        # ... more error messages
    }
}
```

Standardized messages for consistent user feedback.

## Using Constants

### Import Constants
```python
from src.core.constants import DECK_SIZE, MAX_CARD_COPIES, STRATEGIES, COLORS
```

### In Deck Building
```python
def build_deck(strategy):
    strategy_config = STRATEGIES[strategy.upper()]
    character_count = int(DECK_SIZE * strategy_config['character_ratio'])
    # ... build deck
```

### In Validation
```python
def validate_deck(deck):
    if len(deck) != DECK_SIZE:
        return f"Deck must contain exactly {DECK_SIZE} cards"
    
    card_counts = {}
    for card in deck:
        if card['name'] in card_counts:
            card_counts[card['name']] += 1
            if card_counts[card['name']] > MAX_CARD_COPIES:
                return f"Cannot have more than {MAX_CARD_COPIES} copies"
```

### In API Responses
```python
from src.core.constants import MESSAGES

return jsonify({
    'success': True,
    'message': MESSAGES['SUCCESS']['USER_REGISTERED']
})
```

## Key Principles

### 1. Single Source of Truth
All magic numbers and hardcoded values are defined here:
- No duplicate constants across files
- Easy to update values in one place
- Consistent values throughout application

### 2. Semantic Naming
Constants have descriptive names:
- `DECK_SIZE` not `DS` or `50`
- `MAX_CARD_COPIES` not `MAX_C` or `4`
- `AGGRESSIVE` not `AGG` or `1`

### 3. Organization
Constants are grouped logically:
- Card-related constants together
- Strategy configurations grouped
- Messages categorized by type

### 4. Immutability
Constants should not be modified at runtime:
- Use uppercase names (Python convention)
- Use tuples or frozensets for collections where appropriate
- Define as module-level variables

## Adding New Constants

When adding new constants:

1. **Choose appropriate file** (currently only `constants.py`)
2. **Use descriptive names** in UPPER_SNAKE_CASE
3. **Group with related constants**
4. **Add documentation** (comment or docstring)
5. **Update this README** if adding new categories

Example:
```python
# Tournament Settings
TOURNAMENT_MODE_ENABLED = True
TOURNAMENT_DECK_SIZE = 50
TOURNAMENT_BANNED_CARDS = [
    'Card Name 1',
    'Card Name 2'
]

# Simulation Settings
DEFAULT_SIMULATION_COUNT = 1000
MAX_SIMULATION_COUNT = 10000
SIMULATION_TIMEOUT = 30  # seconds
```

## Configuration vs Constants

### Use Constants for:
- Values that never change (deck size, max copies)
- Enumerations (card types, colors)
- Application-wide defaults
- Message templates

### Use Configuration for:
- Environment-specific settings (database URLs)
- Values that might change between deployments
- Feature flags
- Performance tuning parameters

See [Configuration Documentation](../config/README.md) for configuration management.

## Strategy Configuration

Strategy configurations define deck building behavior:

### Fields
- `name` - Strategy identifier
- `character_ratio` - Percentage of characters (0.0-1.0)
- `event_ratio` - Percentage of events (0.0-1.0)
- `stage_ratio` - Percentage of stages (0.0-1.0)
- `avg_cost_target` - Target average card cost
- `low_cost_preference` - Prefer low-cost cards

### Usage
```python
from src.core.constants import STRATEGIES

strategy = STRATEGIES['AGGRESSIVE']
target_characters = int(DECK_SIZE * strategy['character_ratio'])
```

### Adding New Strategy
```python
STRATEGIES['MIDRANGE'] = {
    'name': 'midrange',
    'character_ratio': 0.68,
    'event_ratio': 0.28,
    'stage_ratio': 0.04,
    'avg_cost_target': 4.0,
    'low_cost_preference': False
}
```

## Error Messages

Standardized error messages ensure consistency:

### Benefits
- Consistent user experience
- Easy to update messages
- Supports internationalization (future)
- Clear error communication

### Usage
```python
from src.core.constants import MESSAGES

if not username:
    return (False, None, MESSAGES['ERROR']['MISSING_USERNAME'])
```

## Related Documentation

- [Configuration](../config/README.md) - Environment-based settings
- [Services](../services/README.md) - Business logic using constants
- [Architecture](../../docs/architecture/ARCHITECTURE.md) - Overall structure
- [One Piece TCG Rules](../../docs/guides/ONE_PIECE_TCG_RULES.md) - Game rules implementation
