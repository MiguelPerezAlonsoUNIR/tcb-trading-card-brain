# Services (src/services/)

This directory contains the business logic layer of the application. Services encapsulate all business rules and orchestrate operations between the API layer and the database models.

## Service Classes

### auth_service.py
Authentication and user management business logic.

**Key Methods:**
- `register_user(username, password)` - Register a new user with validation
- `login_user(username, password)` - Authenticate user credentials
- `validate_username(username)` - Validate username format and availability
- `validate_password(password)` - Validate password strength

**Returns:** Tuple of `(success: bool, result: Any, error: str)`

### deck_service.py
Deck management business logic.

**Key Methods:**
- `create_deck(user_id, deck_data)` - Create and save a new deck
- `get_user_decks(user_id)` - Get all decks for a user
- `get_deck_by_id(deck_id, user_id)` - Get specific deck with ownership check
- `update_deck(deck_id, user_id, updates)` - Update deck with ownership check
- `delete_deck(deck_id, user_id)` - Delete deck with ownership check

**Returns:** Tuple of `(success: bool, result: Any, error: str)`

### collection_service.py
Card collection management business logic.

**Key Methods:**
- `get_user_collection(user_id)` - Get user's complete collection
- `add_or_update_card(user_id, card_name, quantity)` - Add/update card with validation
- `remove_card(collection_id, user_id)` - Remove card with ownership check
- `build_deck_from_collection(user_id, strategy, color)` - Build deck from owned cards

**Returns:** Tuple of `(success: bool, result: Any, error: str)`

### card_service.py
Card database management business logic.

**Key Methods:**
- `get_all_cards(filters)` - Get cards with optional filtering
- `get_card_by_id(card_id)` - Get specific card
- `create_card(card_data)` - Add new card with validation
- `update_card(card_id, updates)` - Update existing card
- `delete_card(card_id)` - Delete card (checks for references)
- `get_or_create_card_set(set_code, set_name, release_date)` - Manage card sets

**Returns:** Tuple of `(success: bool, result: Any, error: str)`

## Service Pattern

All services follow a consistent pattern:

### Method Signature
```python
@staticmethod
def operation_name(params) -> tuple[bool, Any, str]:
    """
    Brief description.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        tuple: (success, result, error_message)
            - success: True if operation succeeded
            - result: The result object (model, list, etc.) or None
            - error_message: Error description or None
    """
```

### Return Pattern
Services always return a tuple with three elements:
1. **success (bool)**: Whether the operation succeeded
2. **result (Any)**: The result data (model instance, list, dict, etc.) or None on failure
3. **error (str)**: Error message on failure, None on success

### Example Usage
```python
# In a route
success, user, error = AuthService.register_user(username, password)
if success:
    return jsonify({'success': True, 'user': user.to_dict()})
else:
    return jsonify({'success': False, 'error': error}), 400
```

## Key Principles

### 1. Separation of Concerns
- **Services contain business logic only**
- No HTTP request/response handling
- No direct database commits (except within methods)
- Reusable across different interfaces

### 2. Transaction Management
Services handle database transactions:
```python
try:
    # Create and add objects
    db.session.add(new_object)
    db.session.commit()
    return (True, new_object, None)
except Exception as e:
    db.session.rollback()
    return (False, None, str(e))
```

### 3. Validation
Services perform all validation:
- Input validation
- Business rule validation
- Data integrity checks
- Authorization checks

### 4. Consistent Error Handling
- Clear, user-friendly error messages
- Consistent error formats
- Proper exception handling
- Database rollback on errors

### 5. Testability
Services are easily testable:
- No dependency on Flask context
- Can be tested in isolation
- Mock database if needed
- Clear input/output contracts

## Adding New Services

When adding a new service:

1. **Create service file** in `src/services/`
2. **Use static methods** for stateless operations
3. **Follow return pattern**: `(success, result, error)`
4. **Add validation** for all inputs
5. **Handle transactions** properly
6. **Write comprehensive tests**
7. **Document methods** with docstrings

Example template:
```python
from src.models import db, MyModel

class MyService:
    """Service for managing MyModel operations."""
    
    @staticmethod
    def create_item(data: dict) -> tuple[bool, MyModel, str]:
        """
        Create a new item.
        
        Args:
            data: Dictionary containing item data
            
        Returns:
            tuple: (success, item, error)
        """
        # Validation
        if not data.get('required_field'):
            return (False, None, "Required field missing")
        
        try:
            # Business logic
            item = MyModel(**data)
            db.session.add(item)
            db.session.commit()
            return (True, item, None)
        except Exception as e:
            db.session.rollback()
            return (False, None, str(e))
```

## Testing Services

Services should have comprehensive unit tests:

```python
def test_create_item_success():
    success, item, error = MyService.create_item({'required_field': 'value'})
    assert success is True
    assert item is not None
    assert error is None

def test_create_item_validation_error():
    success, item, error = MyService.create_item({})
    assert success is False
    assert item is None
    assert 'Required field missing' in error
```

## Related Documentation

- [API Routes](../api/routes/README.md) - How services are called from routes
- [Models](../models/README.md) - Database models used by services
- [Architecture](../../docs/architecture/ARCHITECTURE.md) - Overall architecture
- [Testing Guide](../../tests/TESTING.md) - How to test services
