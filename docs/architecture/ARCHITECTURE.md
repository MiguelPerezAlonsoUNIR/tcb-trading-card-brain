# Project Architecture

## Overview

This document describes the improved architecture of the TCB Trading Card Brain application. The project has been refactored to follow best practices for maintainability, scalability, and testability.

## Architecture Principles

1. **Separation of Concerns**: Business logic, data access, and presentation layers are clearly separated
2. **Modularity**: Code is organized into cohesive modules with clear responsibilities
3. **Single Responsibility**: Each module/class has a single, well-defined purpose
4. **Dependency Injection**: Dependencies are injected rather than hard-coded
5. **Configuration Management**: All configuration is centralized
6. **API Versioning Ready**: Structure supports future API versioning

## Directory Structure

```
tcb-trading-card-brain/
├── src/                        # Source code package
│   ├── __init__.py
│   ├── api/                    # API layer
│   │   ├── __init__.py
│   │   ├── utils.py           # API utilities (decorators, helpers)
│   │   └── routes/            # API route blueprints
│   │       ├── __init__.py
│   │       ├── auth_routes.py      # Authentication endpoints
│   │       ├── deck_routes.py      # Deck management endpoints
│   │       ├── collection_routes.py # Collection endpoints
│   │       ├── card_routes.py      # Card database endpoints
│   │       └── game_routes.py      # Game-related endpoints
│   ├── config/                 # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py        # Environment-based configuration
│   ├── core/                   # Core utilities and constants
│   │   ├── __init__.py
│   │   └── constants.py       # Application constants
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   └── models.py          # SQLAlchemy models
│   └── services/               # Business logic layer
│       ├── __init__.py
│       ├── auth_service.py    # Authentication business logic
│       ├── deck_service.py    # Deck management logic
│       ├── collection_service.py # Collection management logic
│       └── card_service.py    # Card database logic
├── tests/                      # Test suite (future organization)
├── templates/                  # HTML templates
├── static/                     # Static assets (CSS, JS, images)
├── app.py                      # Application entry point
├── deck_builder.py             # Deck building AI logic
├── combat_simulator.py         # Combat simulation logic
├── structure_decks.py          # Structure deck definitions
├── cards_data.py              # Card database
├── requirements.txt           # Python dependencies
└── README.md                  # Main documentation
```

## Layer Responsibilities

### 1. API Layer (`src/api/`)

**Purpose**: Handle HTTP requests/responses and route to appropriate services

**Components**:
- **Route Blueprints**: Organize endpoints by domain (auth, decks, collections, cards, game)
- **Utilities**: Common decorators (e.g., `@login_required_api`) and helpers
- **Request Validation**: Validate incoming request data
- **Response Formatting**: Format responses consistently

**Key Principles**:
- Routes should be thin - delegate to services
- No business logic in routes
- Consistent error handling
- Use blueprints for modularity

### 2. Service Layer (`src/services/`)

**Purpose**: Implement business logic and orchestrate operations

**Components**:
- **AuthService**: User registration, login, logout, password management
- **DeckService**: Deck CRUD operations
- **CollectionService**: Collection management
- **CardService**: Card database operations

**Key Principles**:
- All business logic lives here
- Methods return tuples: `(success, result, error_message)`
- No direct request/response handling
- Transaction management (commit/rollback)
- Reusable across different interfaces (API, CLI, etc.)

### 3. Models Layer (`src/models/`)

**Purpose**: Define data structures and database schema

**Components**:
- **Database Models**: User, Deck, UserCollection, Card, CardSet
- **Model Methods**: Helper methods for serialization (`to_dict()`)
- **Relationships**: Define relationships between entities

**Key Principles**:
- Pure data models - no business logic
- Clear relationships between entities
- Helper methods for data conversion
- Database constraints defined here

### 4. Configuration Layer (`src/config/`)

**Purpose**: Centralize all application configuration

**Components**:
- **Config Classes**: Base, Development, Production, Test configurations
- **Environment Detection**: Automatically select config based on FLASK_ENV
- **Constants**: Game rules, pagination, timeouts, etc.

**Key Principles**:
- All magic values centralized
- Environment-specific overrides
- Type-safe configuration access
- Easy to modify without touching code

### 5. Core Layer (`src/core/`)

**Purpose**: Shared utilities and constants

**Components**:
- **Constants**: Card types, colors, strategies, API messages
- **Strategy Configuration**: Deck building strategy parameters
- **Error Messages**: Centralized error message definitions

**Key Principles**:
- No business logic
- Imported by multiple layers
- Single source of truth for constants

## Design Patterns

### 1. Application Factory Pattern

The `create_app()` function in `app.py` creates and configures the Flask application:

```python
def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class or get_config())
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    register_blueprints(app)
    
    return app
```

**Benefits**:
- Easy testing with different configurations
- Multiple app instances possible
- Clean initialization flow

### 2. Blueprint Pattern

Routes are organized into blueprints by domain:

```python
auth_bp = Blueprint('auth', __name__)
deck_bp = Blueprint('decks', __name__)
```

**Benefits**:
- Modular route organization
- Easy to add/remove features
- Clear URL structure
- Ready for API versioning

### 3. Service Pattern

Business logic is encapsulated in service classes:

```python
class AuthService:
    @staticmethod
    def register_user(username, password):
        # Validation
        # Create user
        # Return (success, user, error)
```

**Benefits**:
- Testable without HTTP layer
- Reusable across interfaces
- Clear separation of concerns
- Transaction management in one place

### 4. Repository Pattern (Implicit)

Services act as repositories for data access:

```python
class DeckService:
    @staticmethod
    def get_user_decks(user_id):
        return Deck.query.filter_by(user_id=user_id).all()
```

**Benefits**:
- Abstract database operations
- Easy to swap data sources
- Centralized query logic

## Configuration Management

Configuration is environment-aware and centralized:

```python
# Development
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tcb.db'

# Production
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

**Access Configuration**:
```python
app.config['DECK_SIZE']  # 50
app.config['MAX_CARD_COPIES']  # 4
```

## API Structure

### Endpoint Organization

- `/api/register`, `/api/login`, `/api/logout` - Authentication
- `/api/decks` - Deck management
- `/api/collection` - Collection management
- `/api/admin/cards` - Card database (admin)
- `/api/build-deck`, `/api/analyze-deck` - Game features

### Response Format

All API responses follow a consistent format:

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

### Error Handling

Errors are handled consistently:

```python
return jsonify({
    'success': False,
    'error': 'User-friendly error message'
}), 400
```

## Testing Strategy

### Current State
- 20 tests passing
- Tests located in root directory (to be migrated)
- Good coverage of core functionality

### Future Organization
```
tests/
├── unit/                  # Unit tests for individual components
│   ├── test_services/
│   ├── test_models/
│   └── test_utils/
├── integration/           # Integration tests
│   ├── test_api/
│   └── test_database/
└── e2e/                   # End-to-end tests
```

## Backwards Compatibility

To maintain compatibility with existing tests and scripts:

1. **auth.py**: Wrapper that imports from `src.services.AuthService`
2. **models.py**: Wrapper that imports from `src.models`
3. **Root-level files**: Legacy files maintained temporarily

These can be removed once all references are updated.

## Migration Guide

### For New Features

1. **Add a new API endpoint**:
   - Create route in appropriate blueprint (`src/api/routes/`)
   - Implement business logic in service (`src/services/`)
   - Add constants to `src/core/constants.py`

2. **Add a new database model**:
   - Add model to `src/models/models.py`
   - Create migration (if using Alembic)
   - Add service methods for CRUD operations

3. **Add configuration**:
   - Add to `src/config/settings.py`
   - Use via `app.config['YOUR_KEY']`

### For Existing Code

1. Update imports:
   ```python
   # Old
   from models import db, User
   from auth import login_required_api
   
   # New
   from src.models import db, User
   from src.api.utils import login_required_api
   ```

2. Use services for business logic:
   ```python
   # Old
   user = User(username=username, password_hash=hash_password(password))
   db.session.add(user)
   db.session.commit()
   
   # New
   success, user, error = AuthService.register_user(username, password)
   ```

## Benefits of New Architecture

1. **Maintainability**:
   - Clear structure makes finding code easy
   - Changes isolated to specific layers
   - Reduced coupling between components

2. **Testability**:
   - Service layer testable without HTTP
   - Easy to mock dependencies
   - Clear interfaces

3. **Scalability**:
   - Easy to add new features
   - Ready for microservices if needed
   - Support for API versioning

4. **Code Quality**:
   - Single Responsibility Principle
   - DRY (Don't Repeat Yourself)
   - Clear separation of concerns

5. **Developer Experience**:
   - Easy onboarding for new developers
   - Consistent patterns throughout
   - Self-documenting structure

## Future Enhancements

1. **API Versioning**: Add `/api/v1/`, `/api/v2/` structure
2. **Dependency Injection**: Use Flask-Injector for DI
3. **Caching Layer**: Add Redis for caching
4. **Message Queue**: Add Celery for async tasks
5. **Microservices**: Extract services into separate apps
6. **GraphQL**: Add GraphQL API alongside REST
7. **Database Migrations**: Add Alembic for migrations
8. **Monitoring**: Add application monitoring (Sentry, DataDog)

## Conclusion

This refactored architecture provides a solid foundation for future development while maintaining all existing functionality. The modular structure makes the codebase more maintainable, testable, and scalable.
