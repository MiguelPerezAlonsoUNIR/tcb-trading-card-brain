# Source Code (src/)

This directory contains the main application source code organized in a modular architecture.

## Directory Structure

```
src/
├── api/                    # API layer (routes, blueprints)
│   ├── routes/            # Organized route blueprints
│   └── utils.py           # API utilities and decorators
├── config/                 # Configuration management
│   └── settings.py        # Environment-based configuration
├── core/                   # Core utilities and constants
│   └── constants.py       # Application constants
├── models/                 # Database models
│   └── models.py          # SQLAlchemy models
└── services/               # Business logic layer
    ├── auth_service.py    # Authentication business logic
    ├── card_service.py    # Card database logic
    ├── collection_service.py # Collection management logic
    └── deck_service.py    # Deck management logic
```

## Package Overview

### API Layer (`api/`)

Handles HTTP requests/responses and routes to appropriate services.

- **Route Blueprints**: Organize endpoints by domain (auth, decks, collections, cards, game)
- **Utilities**: Common decorators (e.g., `@login_required_api`) and helpers
- **Request Validation**: Validate incoming request data
- **Response Formatting**: Format responses consistently

**Key Principle**: Routes should be thin - delegate to services. No business logic in routes.

### Configuration Layer (`config/`)

Centralizes all application configuration.

- **Config Classes**: Base, Development, Production, Test configurations
- **Environment Detection**: Automatically select config based on FLASK_ENV
- **Constants**: Game rules, pagination, timeouts, etc.

### Core Layer (`core/`)

Shared utilities and constants used across the application.

- **Constants**: Card types, colors, strategies, API messages
- **Strategy Configuration**: Deck building strategy parameters
- **Error Messages**: Centralized error message definitions

### Models Layer (`models/`)

Defines data structures and database schema.

- **Database Models**: User, Deck, UserCollection, Card, CardSet
- **Model Methods**: Helper methods for serialization (`to_dict()`)
- **Relationships**: Define relationships between entities

**Key Principle**: Pure data models - no business logic.

### Services Layer (`services/`)

Implements business logic and orchestrates operations.

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

## Design Patterns

The source code follows these key patterns:

1. **Service Pattern**: Business logic encapsulated in service classes
2. **Blueprint Pattern**: Routes organized into blueprints by domain
3. **Repository Pattern**: Services act as repositories for data access
4. **Dependency Injection**: Dependencies injected rather than hard-coded

## Related Documentation

- [Architecture Documentation](../docs/architecture/ARCHITECTURE.md) - Detailed architecture overview
- [API Documentation](../docs/api/CARD_DATABASE.md) - API endpoints and database schema
- [Testing Guide](../tests/TESTING.md) - How to test the application

## Getting Started

To work with the source code:

1. Install dependencies: `pip install -r requirements.txt`
2. Review the [Architecture Documentation](../docs/architecture/ARCHITECTURE.md)
3. Look at service layer for business logic examples
4. Follow existing patterns when adding new features

## Adding New Features

When adding new features:

1. **Add API endpoint**: Create route in appropriate blueprint (`src/api/routes/`)
2. **Implement business logic**: Add methods to appropriate service (`src/services/`)
3. **Define models**: Add database models if needed (`src/models/models.py`)
4. **Add constants**: Add configuration to `src/core/constants.py`
5. **Write tests**: Add unit tests for services, integration tests for API endpoints
