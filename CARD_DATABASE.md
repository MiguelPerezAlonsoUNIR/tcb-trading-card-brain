# Card Database System

This document describes the database-backed card storage system implemented for TCB Trading Card Brain.

## Overview

The application now uses a SQLite database (upgradeable to PostgreSQL/MySQL) to store all trading card information. This allows for:

- Easy addition of new cards through API endpoints
- Support for multiple card sets and expansions
- Scalable storage that can grow as new sets are released
- Better data integrity with proper database constraints
- Efficient querying and filtering of cards

## Database Schema

### Tables

#### 1. `card_sets` - Card Set/Expansion Information
Stores information about card sets and expansions (e.g., "Romance Dawn", "Paramount War").

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `code` | String(20) | Unique set code (e.g., "OP01", "ST01") |
| `name` | String(200) | Set name |
| `release_date` | Date | Release date (optional) |
| `created_at` | DateTime | Timestamp when added |

#### 2. `cards` - Trading Card Information
Stores all card data including stats, effects, and metadata.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String(200) | Card name |
| `card_type` | String(50) | Leader, Character, Event, or Stage |
| `colors` | String(200) | JSON array of colors |
| `power` | Integer | Power for Characters and Leaders |
| `cost` | Integer | Play cost |
| `life` | Integer | Life points for Leaders |
| `attribute` | String(50) | Strike, Slash, Special, etc. |
| `effect` | Text | Card effect description |
| `set_id` | Integer | Foreign key to `card_sets` |
| `card_number` | String(20) | Card number within set |
| `rarity` | String(50) | Common, Rare, Super Rare, etc. |
| `image_url` | String(500) | URL to card image |
| `created_at` | DateTime | Timestamp when added |

**Constraints:**
- Unique constraint on (`set_id`, `card_number`) - prevents duplicate cards

#### 3. `user_collections` - User Card Collections
Links users to cards they own (existing table, unchanged).

## Getting Started

### Initial Setup

1. **Install dependencies** (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database**:
   ```bash
   python init_cards_db.py
   ```

   This will:
   - Create all database tables
   - Import existing cards from `cards_data.py`
   - Set up card sets
   - Display import statistics

### Database File Location

By default, the database is stored as `tcb.db` in the application root directory. You can change this by setting the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="sqlite:///path/to/your/database.db"
# Or for PostgreSQL:
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

## Managing Cards

### API Endpoints

All card management endpoints are under `/api/admin/`:

#### List All Cards
```bash
GET /api/admin/cards

# With filters:
GET /api/admin/cards?type=Character
GET /api/admin/cards?color=Red
GET /api/admin/cards?set=OP01
```

#### Add a New Card
```bash
POST /api/admin/cards
Content-Type: application/json

{
  "name": "New Card Name",
  "type": "Character",
  "colors": ["Red", "Blue"],
  "power": 5000,
  "cost": 4,
  "attribute": "Strike",
  "effect": "Card effect description",
  "set": "OP03",
  "card_number": "100",
  "rarity": "Rare",
  "image_url": "https://example.com/card.png"
}
```

**Required fields:** `name`, `type`, `colors`, `cost`, `set`, `card_number`

**Optional fields:** `power`, `life`, `attribute`, `effect`, `rarity`, `image_url`

#### Update a Card
```bash
PUT /api/admin/cards/<card_id>
Content-Type: application/json

{
  "power": 6000,
  "effect": "Updated effect"
}
```

#### Delete a Card
```bash
DELETE /api/admin/cards/<card_id>
```

#### List Card Sets
```bash
GET /api/admin/card-sets
```

#### Add a Card Set
```bash
POST /api/admin/card-sets
Content-Type: application/json

{
  "code": "OP03",
  "name": "Pillars of Strength",
  "release_date": "2024-03-01"
}
```

**Note:** Card sets are automatically created when you add a card with a new set code. This endpoint is useful if you want to pre-define a set with a specific name and release date.

### Examples

#### Add a new expansion

1. First, create the set (optional, will be auto-created if you skip):
```bash
curl -X POST http://localhost:5000/api/admin/card-sets \
  -H "Content-Type: application/json" \
  -d '{
    "code": "OP03",
    "name": "Pillars of Strength",
    "release_date": "2024-03-01"
  }'
```

2. Add cards to the set:
```bash
curl -X POST http://localhost:5000/api/admin/cards \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Whitebeard",
    "type": "Leader",
    "colors": ["Red", "Green"],
    "power": 5000,
    "life": 5,
    "cost": 0,
    "attribute": "Strike",
    "effect": "Your Characters with cost 5 or more gain +1000 power",
    "set": "OP03",
    "card_number": "001",
    "rarity": "Leader",
    "image_url": "https://en.onepiece-cardgame.com/images/cardlist/OP03-001.png"
  }'
```

#### Bulk import cards

Create a script to import multiple cards:

```python
import requests
import json

cards = [
    {
        "name": "Card 1",
        "type": "Character",
        "colors": ["Red"],
        "power": 4000,
        "cost": 3,
        "set": "OP03",
        "card_number": "010",
        "rarity": "Common"
    },
    # ... more cards
]

for card in cards:
    response = requests.post(
        'http://localhost:5000/api/admin/cards',
        json=card
    )
    if response.status_code == 201:
        print(f"✓ Added: {card['name']}")
    else:
        print(f"✗ Failed: {card['name']} - {response.json()}")
```

## Using the Database in Code

### In Python (with Flask context)

```python
from app import app, db
from models import Card, CardSet

with app.app_context():
    # Query all cards
    all_cards = Card.query.all()
    
    # Query by type
    leaders = Card.query.filter_by(card_type='Leader').all()
    
    # Query by set
    op01_set = CardSet.query.filter_by(code='OP01').first()
    op01_cards = Card.query.filter_by(set_id=op01_set.id).all()
    
    # Convert to dict
    card_dict = all_cards[0].to_dict()
    print(card_dict)
```

### With Deck Builder

The deck builder automatically loads cards from the database:

```python
from deck_builder import OnePieceDeckBuilder
from app import db

# Create deck builder with database session
deck_builder = OnePieceDeckBuilder(db_session=db.session)

# Cards are automatically loaded from database
all_cards = deck_builder.get_all_cards()
```

## Migration from Hardcoded Cards

The `cards_data.py` file still exists for:
1. **Backward compatibility** - existing code that imports from it will still work
2. **Initial data source** - used by `init_cards_db.py` to populate the database
3. **Fallback** - if no database session is provided to the deck builder

Once you've initialized the database with `init_cards_db.py`, all card operations use the database.

## Data Integrity

The database enforces several constraints:

1. **Unique set codes** - Each card set must have a unique code
2. **Unique card numbers within sets** - Prevents duplicate cards (e.g., two different cards with OP01-001)
3. **Foreign key integrity** - Cards must belong to valid card sets
4. **Required fields** - Ensures essential card data is present

## Testing

Run the test suite to verify database operations:

```bash
# Test card database operations
python test_card_database.py

# Test deck builder integration
python test_deck_builder.py

# Test authentication and user features
python test_auth.py
```

## Performance Considerations

- **Indexing**: The database includes indexes on commonly queried fields (`set_id`, `card_type`, `card_name`)
- **Caching**: The deck builder caches loaded cards in memory for performance
- **Query optimization**: Use filters and joins efficiently when querying large card collections

## Future Enhancements

Potential improvements to the card database system:

1. **Card versioning** - Track different versions/printings of the same card
2. **Card legality** - Mark cards as legal/banned for different formats
3. **Advanced search** - Full-text search on card effects
4. **Price tracking** - Store and track card market prices
5. **Card images** - Store images locally or integrate with card image APIs
6. **Import/export** - Bulk import from CSV/JSON files
7. **Multi-TCG support** - Extend to support multiple trading card games

## Troubleshooting

### Database not found
```
Error: no such table: cards
```
**Solution:** Run `python init_cards_db.py` to create tables and import cards

### Duplicate card error
```
Error: UNIQUE constraint failed
```
**Solution:** A card with the same set code and card number already exists. Use PUT to update it instead.

### Missing card set
```
Error: Card set not found
```
**Solution:** Create the card set first, or let it be auto-created when adding a card

## Support

For issues or questions about the card database system:
1. Check this documentation
2. Run the test suite to verify your setup
3. Check database integrity with `python init_cards_db.py` (won't add duplicates)
4. Open an issue on the project repository
