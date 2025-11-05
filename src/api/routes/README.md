# API Routes (src/api/routes/)

This directory contains Flask Blueprint definitions for all API endpoints, organized by domain.

## Route Blueprints

### auth_routes.py
Authentication and user management endpoints.

**Endpoints:**
- `POST /api/register` - Register a new user
- `POST /api/login` - Login with credentials
- `POST /api/logout` - Logout current user
- `GET /api/current-user` - Get current user information

**Related Service:** `AuthService` in `src/services/auth_service.py`

### deck_routes.py
Deck management endpoints for authenticated users.

**Endpoints:**
- `GET /api/decks` - Get all decks for current user
- `POST /api/decks` - Save a new deck
- `GET /api/decks/<id>` - Get a specific deck
- `PUT /api/decks/<id>` - Update a specific deck
- `DELETE /api/decks/<id>` - Delete a specific deck

**Related Service:** `DeckService` in `src/services/deck_service.py`

**Authentication:** All endpoints require authentication

### collection_routes.py
Card collection management endpoints.

**Endpoints:**
- `GET /api/collection` - Get user's card collection
- `POST /api/collection` - Add or update card in collection
- `DELETE /api/collection/<id>` - Remove card from collection
- `POST /api/suggest-deck` - Build deck based on user's collection

**Related Service:** `CollectionService` in `src/services/collection_service.py`

**Authentication:** All endpoints require authentication

### card_routes.py
Card database management endpoints (admin functions).

**Endpoints:**
- `GET /api/admin/cards` - List all cards (with optional filters)
- `POST /api/admin/cards` - Add a new card
- `PUT /api/admin/cards/<id>` - Update an existing card
- `DELETE /api/admin/cards/<id>` - Delete a card
- `GET /api/admin/card-sets` - List all card sets
- `POST /api/admin/card-sets` - Add a new card set

**Related Service:** `CardService` in `src/services/card_service.py`

**Note:** These are admin endpoints for managing the card database

### game_routes.py
Game-related endpoints including deck building, analysis, and simulation.

**Public Endpoints:**
- `GET /api/cards` - Get all available cards with images
- `POST /api/build-deck` - Build a deck based on preferences
- `POST /api/analyze-deck` - Analyze a deck and provide suggestions
- `POST /api/suggest-improvements` - Get three improved deck variations
- `GET /api/opponent-decks` - Get tournament opponent decks
- `POST /api/simulate-combat` - Run combat simulation

**Related Services:**
- Deck building logic in `deck_builder.py`
- Combat simulation in `combat_simulator.py`

## Blueprint Registration

All blueprints are registered in `src/api/__init__.py` and imported by the main application in `app.py`.

```python
from src.api.routes.auth_routes import auth_bp
from src.api.routes.deck_routes import deck_bp
from src.api.routes.collection_routes import collection_bp
from src.api.routes.card_routes import card_bp
from src.api.routes.game_routes import game_bp

app.register_blueprint(auth_bp)
app.register_blueprint(deck_bp)
app.register_blueprint(collection_bp)
app.register_blueprint(card_bp)
app.register_blueprint(game_bp)
```

## Common Patterns

### Authentication
Routes requiring authentication use the `@login_required_api` decorator:

```python
from src.api.utils import login_required_api

@deck_bp.route('/api/decks', methods=['GET'])
@login_required_api
def get_decks():
    # Only authenticated users can access
```

### Response Format
All API endpoints return JSON responses with consistent structure:

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error message"
}
```

### Request Validation
Routes validate incoming data and return 400 errors for invalid requests:

```python
data = request.get_json()
if not data or 'required_field' not in data:
    return jsonify({'success': False, 'error': 'Missing required field'}), 400
```

### Service Layer Delegation
Routes delegate business logic to services:

```python
success, result, error = DeckService.create_deck(user_id, deck_data)
if success:
    return jsonify({'success': True, 'deck': result.to_dict()})
else:
    return jsonify({'success': False, 'error': error}), 400
```

## Adding New Routes

When adding new API endpoints:

1. **Choose the appropriate blueprint** or create a new one if needed
2. **Define the route** with appropriate HTTP method
3. **Add authentication** decorator if required
4. **Validate request data** before processing
5. **Delegate to service layer** for business logic
6. **Return consistent JSON** response format
7. **Add error handling** for expected failure cases
8. **Document the endpoint** in this README

## Testing

API routes should be tested with:
- **Unit tests**: Test route logic in isolation (mock services)
- **Integration tests**: Test complete request/response cycle
- **System tests**: Test with real database (in `tests/system/`)

See [Testing Guide](../../../tests/TESTING.md) for more information.

## Related Documentation

- [API Documentation](../../../docs/api/CARD_DATABASE.md) - Detailed API reference
- [Architecture](../../../docs/architecture/ARCHITECTURE.md) - Overall architecture
- [Services](../../services/README.md) - Business logic layer
- [Models](../../models/README.md) - Database models
