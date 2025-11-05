# Models (src/models/)

This directory contains the database models (schema definitions) for the application using SQLAlchemy ORM.

## Model Files

### models.py
Contains all database model definitions.

**Models:**
- `User` - User accounts and authentication
- `Deck` - User's saved decks
- `UserCollection` - Cards owned by users
- `Card` - Trading card information
- `CardSet` - Card sets/expansions

## Database Models

### User
User account information and authentication.

**Fields:**
- `id` (Integer, Primary Key) - User ID
- `username` (String, Unique) - Username
- `password_hash` (String) - Hashed password
- `created_at` (DateTime) - Account creation timestamp

**Relationships:**
- `decks` - One-to-many with Deck
- `collection` - One-to-many with UserCollection

**Methods:**
- `set_password(password)` - Hash and set password
- `check_password(password)` - Verify password
- `to_dict()` - Convert to dictionary

### Deck
User's saved deck configurations.

**Fields:**
- `id` (Integer, Primary Key) - Deck ID
- `user_id` (Integer, Foreign Key) - Owner user ID
- `name` (String) - Deck name
- `strategy` (String) - Strategy type (balanced/aggressive/control)
- `color` (String) - Primary color(s)
- `leader` (JSON) - Leader card data
- `main_deck` (JSON) - Main deck cards
- `created_at` (DateTime) - Creation timestamp

**Relationships:**
- `user` - Many-to-one with User

**Methods:**
- `to_dict()` - Convert to dictionary

### UserCollection
Cards owned by users.

**Fields:**
- `id` (Integer, Primary Key) - Collection entry ID
- `user_id` (Integer, Foreign Key) - Owner user ID
- `card_name` (String) - Name of the card
- `quantity` (Integer) - Number of copies owned
- `added_at` (DateTime) - When added to collection

**Relationships:**
- `user` - Many-to-one with User

**Methods:**
- `to_dict()` - Convert to dictionary

### Card
Trading card information.

**Fields:**
- `id` (Integer, Primary Key) - Card ID
- `name` (String) - Card name
- `card_type` (String) - Type (Leader/Character/Event/Stage)
- `colors` (String) - JSON array of colors
- `power` (Integer) - Power value
- `cost` (Integer) - Play cost
- `life` (Integer) - Life points (for Leaders)
- `attribute` (String) - Attribute (Strike/Slash/Special/etc.)
- `effect` (Text) - Card effect description
- `set_id` (Integer, Foreign Key) - Card set ID
- `card_number` (String) - Card number within set
- `rarity` (String) - Rarity (Common/Rare/Super Rare/etc.)
- `image_url` (String) - URL to card image
- `created_at` (DateTime) - When added to database

**Relationships:**
- `card_set` - Many-to-one with CardSet

**Methods:**
- `to_dict()` - Convert to dictionary

**Constraints:**
- Unique constraint on (set_id, card_number)

### CardSet
Card sets and expansions.

**Fields:**
- `id` (Integer, Primary Key) - Set ID
- `code` (String, Unique) - Set code (e.g., "OP01", "ST01")
- `name` (String) - Set name
- `release_date` (Date) - Release date
- `created_at` (DateTime) - When added to database

**Relationships:**
- `cards` - One-to-many with Card

**Methods:**
- `to_dict()` - Convert to dictionary

## Model Pattern

All models follow consistent patterns:

### Base Configuration
```python
class MyModel(db.Model):
    __tablename__ = 'my_model'
    
    id = db.Column(db.Integer, primary_key=True)
    # ... other fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Relationships
```python
# One-to-many
user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
user = db.relationship('User', backref='items')

# Many-to-one (accessed from parent)
# In User model:
items = db.relationship('MyModel', backref='user', lazy=True)
```

### Serialization
```python
def to_dict(self):
    """Convert model to dictionary."""
    return {
        'id': self.id,
        'field1': self.field1,
        'created_at': self.created_at.isoformat() if self.created_at else None
    }
```

## Database Operations

### Creating Records
```python
from src.models import db, User

user = User(username='john', password_hash='...')
db.session.add(user)
db.session.commit()
```

### Querying Records
```python
# Get all
users = User.query.all()

# Filter
user = User.query.filter_by(username='john').first()

# Multiple conditions
decks = Deck.query.filter_by(user_id=1, color='Red').all()

# Order
cards = Card.query.order_by(Card.name).all()

# Join
decks_with_users = db.session.query(Deck).join(User).all()
```

### Updating Records
```python
user = User.query.get(1)
user.username = 'new_username'
db.session.commit()
```

### Deleting Records
```python
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

## Database Migrations

The application uses SQLAlchemy to create tables:

```python
# In app.py or init script
with app.app_context():
    db.create_all()
```

For production, consider using Alembic for database migrations.

## Key Principles

### 1. Pure Data Models
- Models define data structure only
- No business logic in models
- Helper methods for serialization only

### 2. Relationships
- Define relationships clearly
- Use appropriate cascade behaviors
- Use lazy loading appropriately

### 3. Validation
- Database-level constraints (unique, not null)
- Application-level validation in services

### 4. Serialization
- All models have `to_dict()` method
- Consistent output format
- Handle None values properly

## Adding New Models

When adding a new model:

1. **Define the model class** in `models.py`
2. **Add fields** with appropriate types and constraints
3. **Define relationships** if needed
4. **Add `to_dict()` method** for serialization
5. **Create corresponding service** for business logic
6. **Write tests** for model operations
7. **Update database** (run migrations or `db.create_all()`)

Example template:
```python
class MyModel(db.Model):
    """Description of the model."""
    __tablename__ = 'my_models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='my_models')
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
```

## Testing Models

Models should be tested in system/integration tests:

```python
def test_create_model():
    model = MyModel(name='Test')
    db.session.add(model)
    db.session.commit()
    
    assert model.id is not None
    assert model.name == 'Test'

def test_model_relationships():
    user = User(username='test')
    model = MyModel(name='Test', user=user)
    db.session.add(model)
    db.session.commit()
    
    assert model.user.username == 'test'
    assert len(user.my_models) == 1
```

## Related Documentation

- [Services](../services/README.md) - Business logic that uses models
- [API Documentation](../../docs/api/CARD_DATABASE.md) - API endpoints and schema
- [Architecture](../../docs/architecture/ARCHITECTURE.md) - Overall architecture
- [Testing Guide](../../tests/TESTING.md) - How to test models
