# Test Organization

This directory contains all tests for the TCB Trading Card Brain application, organized by test type.

## Directory Structure

```
tests/
├── unit/           # Unit tests - test individual components in isolation
│   ├── test_50_card_decks.py
│   ├── test_card_images.py
│   ├── test_color_rules.py
│   ├── test_combat_simulator.py
│   ├── test_complete_feature.py
│   ├── test_deck_builder.py
│   ├── test_deck_improvements.py
│   └── test_structure_deck_counts.py
│
└── system/         # System/Integration tests - test full system with Flask app and database
    ├── test_auth.py
    ├── test_card_database.py
    ├── test_improvements_api.py
    ├── test_structure_decks.py
    └── test_tcg_selection.py
```

## Test Types

### Unit Tests (`tests/unit/`)
Unit tests focus on testing individual components in isolation without external dependencies like databases or the Flask application. These tests:
- Don't require Flask or database setup
- Test pure business logic (deck building, combat simulation, etc.)
- Run quickly and independently
- Can be run without installing application dependencies

**Run unit tests:**
```bash
python tests/unit/test_deck_builder.py
python tests/unit/test_color_rules.py
# etc.
```

### System Tests (`tests/system/`)
System/Integration tests verify the full application behavior including Flask routes, API endpoints, and database operations. These tests:
- Require Flask and database dependencies
- Test complete user workflows
- Test API endpoints and authentication
- Require `pip install -r requirements.txt`

**Run system tests:**
```bash
# First install dependencies
pip install -r requirements.txt

# Then run tests
python tests/system/test_auth.py
python tests/system/test_improvements_api.py
# etc.
```

## Running All Tests

### Run all unit tests:
```bash
for test in tests/unit/test_*.py; do
    echo "Running $test..."
    python "$test" || echo "FAILED: $test"
done
```

### Run all system tests:
```bash
# Make sure dependencies are installed first
pip install -r requirements.txt

for test in tests/system/test_*.py; do
    echo "Running $test..."
    python "$test" || echo "FAILED: $test"
done
```

## Adding New Tests

When adding new tests, follow these guidelines:

1. **Unit tests** should go in `tests/unit/` if they:
   - Test individual functions or classes
   - Don't need Flask app context
   - Don't need database access
   - Test pure business logic

2. **System tests** should go in `tests/system/` if they:
   - Test API endpoints
   - Require database operations
   - Test authentication/authorization
   - Test full user workflows
   - Need Flask application context

All test files should:
- Be named with `test_` prefix
- Include the path setup code to import project modules
- Have a docstring explaining what is being tested
- Be executable directly with Python
