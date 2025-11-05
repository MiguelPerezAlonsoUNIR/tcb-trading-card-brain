# Configuration (src/config/)

This directory contains centralized configuration management for the application.

## Configuration Files

### settings.py
Environment-based configuration classes.

**Configuration Classes:**
- `Config` - Base configuration with common settings
- `DevelopmentConfig` - Development environment settings
- `ProductionConfig` - Production environment settings
- `TestConfig` - Testing environment settings

## Configuration Structure

### Base Configuration (Config)
Common settings shared across all environments.

**Key Settings:**
- `SECRET_KEY` - Secret key for session management
- `SQLALCHEMY_TRACK_MODIFICATIONS` - SQLAlchemy setting (False)
- `DECK_SIZE` - Target deck size (50 cards)
- `MAX_CARD_COPIES` - Maximum copies per card (4)
- Game constants (strategies, colors, etc.)

### Development Configuration (DevelopmentConfig)
Settings optimized for local development.

**Settings:**
- `DEBUG = True` - Enable debug mode
- `SQLALCHEMY_DATABASE_URI` - SQLite database for development
- `TESTING = False`

### Production Configuration (ProductionConfig)
Settings for production deployment.

**Settings:**
- `DEBUG = False` - Disable debug mode
- `SQLALCHEMY_DATABASE_URI` - Production database from environment
- Strong `SECRET_KEY` required
- Production-grade security settings

### Test Configuration (TestConfig)
Settings for running tests.

**Settings:**
- `TESTING = True` - Enable testing mode
- `SQLALCHEMY_DATABASE_URI` - In-memory SQLite for tests
- `WTF_CSRF_ENABLED = False` - Disable CSRF for testing

## Environment Detection

Configuration is automatically selected based on the `FLASK_ENV` environment variable:

```python
def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestConfig
    else:
        return DevelopmentConfig
```

## Using Configuration

### In Application Setup
```python
from src.config.settings import get_config

app = Flask(__name__)
app.config.from_object(get_config())
```

### In Application Code
```python
from flask import current_app

# Access configuration
deck_size = current_app.config['DECK_SIZE']
max_copies = current_app.config['MAX_CARD_COPIES']
```

## Configuration Categories

### 1. Security Settings
- `SECRET_KEY` - Session encryption key
- `WTF_CSRF_ENABLED` - CSRF protection toggle
- Password hashing settings

### 2. Database Settings
- `SQLALCHEMY_DATABASE_URI` - Database connection string
- `SQLALCHEMY_TRACK_MODIFICATIONS` - Performance setting

### 3. Application Settings
- `DEBUG` - Debug mode toggle
- `TESTING` - Testing mode toggle
- `JSON_SORT_KEYS` - JSON response sorting

### 4. Game Constants
- `DECK_SIZE` - Required deck size (50)
- `MAX_CARD_COPIES` - Max copies per card (4)
- `STRATEGIES` - Available strategies
- `COLORS` - Available colors

### 5. API Settings
- Rate limiting settings
- Pagination defaults
- Timeout values

## Environment Variables

Configuration can be customized using environment variables:

### Required in Production
- `SECRET_KEY` - Must be set to a strong random value
- `DATABASE_URL` - Production database connection string

### Optional
- `FLASK_ENV` - Environment (development/production/testing)
- `DEBUG` - Override debug mode
- `PORT` - Server port (default: 5000)

### Setting Environment Variables

**Linux/Mac:**
```bash
export FLASK_ENV=production
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="postgresql://user:pass@localhost/db"
```

**Windows:**
```cmd
set FLASK_ENV=production
set SECRET_KEY=your-secret-key-here
set DATABASE_URL=postgresql://user:pass@localhost/db
```

**Docker:**
```dockerfile
ENV FLASK_ENV=production
ENV SECRET_KEY="your-secret-key-here"
```

## Configuration Best Practices

### 1. Environment-Specific Settings
- Use appropriate config class for each environment
- Never use debug mode in production
- Use strong secrets in production

### 2. Sensitive Data
- Never commit secrets to version control
- Use environment variables for sensitive data
- Use `.env` files for local development (add to `.gitignore`)

### 3. Database Configuration
- Use SQLite for development/testing
- Use PostgreSQL/MySQL for production
- Keep database connections in environment variables

### 4. Constants Management
- Define all magic numbers in config
- Use descriptive names
- Group related constants together

## Adding New Configuration

When adding new configuration:

1. **Add to base Config class** if shared across environments
2. **Override in specific config** if environment-dependent
3. **Document the setting** in this README
4. **Use environment variables** for sensitive or deployment-specific values
5. **Provide sensible defaults** where appropriate

Example:
```python
class Config:
    # New feature configuration
    FEATURE_ENABLED = os.environ.get('FEATURE_ENABLED', 'true').lower() == 'true'
    FEATURE_MAX_ITEMS = int(os.environ.get('FEATURE_MAX_ITEMS', '100'))

class ProductionConfig(Config):
    # Override for production if needed
    FEATURE_MAX_ITEMS = int(os.environ.get('FEATURE_MAX_ITEMS', '1000'))
```

## Configuration Validation

Validate critical configuration on startup:

```python
def validate_config(app):
    """Validate critical configuration."""
    if app.config['ENV'] == 'production':
        if app.config['SECRET_KEY'] == 'dev-secret-key-change-in-production':
            raise ValueError("Must set SECRET_KEY in production")
        if app.config['DEBUG']:
            raise ValueError("Must not enable DEBUG in production")
```

## Testing Configuration

Test that configuration is loaded correctly:

```python
def test_development_config():
    app = create_app(DevelopmentConfig)
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is False

def test_production_config():
    app = create_app(ProductionConfig)
    assert app.config['DEBUG'] is False
    assert app.config['TESTING'] is False
```

## Related Documentation

- [Architecture](../../docs/architecture/ARCHITECTURE.md) - Overall architecture
- [Main README](../../README.md) - Environment setup guide
- [Services](../services/README.md) - How services use configuration
