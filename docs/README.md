# Documentation

This directory contains all project documentation organized by topic.

## Documentation Structure

```
docs/
├── README.md              # This file
├── api/                   # API and database documentation
│   └── CARD_DATABASE.md  # Card database system and API endpoints
├── architecture/          # Architecture and design documentation
│   └── ARCHITECTURE.md   # Project architecture overview
├── development/           # Development history and improvement logs
│   ├── IMPROVEMENTS_SUMMARY.md       # Summary of improvements
│   ├── README_STRUCTURE_DECK_FIX.md # Structure deck fixes
│   ├── REFACTORING_COMPLETE.md      # Refactoring documentation
│   └── STRUCTURE_DECK_UPDATE_GUIDE.md # Structure deck update guide
├── features/              # Feature-specific documentation
│   ├── COMBAT_SIMULATION_FEATURE.md  # Combat simulation feature
│   └── DECK_IMPROVEMENTS_FEATURE.md  # Deck improvement feature
└── guides/                # User and developer guides
    └── ONE_PIECE_TCG_RULES.md       # One Piece TCG rules implementation
```

## Quick Links

### For Users
- [Main README](../README.md) - Getting started, features, and usage
- [One Piece TCG Rules](guides/ONE_PIECE_TCG_RULES.md) - Game rules implementation
- [Combat Simulation Feature](features/COMBAT_SIMULATION_FEATURE.md) - How to use combat simulation
- [Deck Improvements Feature](features/DECK_IMPROVEMENTS_FEATURE.md) - How to improve your decks

### For Developers
- [Architecture](architecture/ARCHITECTURE.md) - Project structure and design patterns
- [Card Database](api/CARD_DATABASE.md) - Database schema and API endpoints
- [Development History](development/) - Improvement logs and refactoring notes

### For Testers
- [Testing Guide](../tests/TESTING.md) - How to run tests
- [Test Organization](../tests/README.md) - Test structure and types

## Documentation by Topic

### Architecture & Design
- [ARCHITECTURE.md](architecture/ARCHITECTURE.md) - Complete architecture overview including:
  - Directory structure
  - Layer responsibilities (API, Service, Models, Config, Core)
  - Design patterns used
  - Configuration management
  - Testing strategy
  - Migration guide

### API & Database
- [CARD_DATABASE.md](api/CARD_DATABASE.md) - Card database system including:
  - Database schema
  - API endpoints for card management
  - Card sets and expansions
  - Usage examples
  - Migration from hardcoded cards

### Features
- [COMBAT_SIMULATION_FEATURE.md](features/COMBAT_SIMULATION_FEATURE.md) - Combat simulation including:
  - One Piece TCG rules implementation
  - Monte Carlo simulation
  - Matchup analysis
  - AI insights generation
  - User workflow

- [DECK_IMPROVEMENTS_FEATURE.md](features/DECK_IMPROVEMENTS_FEATURE.md) - Deck improvement system including:
  - Three improvement strategies
  - Collection-based filtering
  - AI-powered suggestions
  - API endpoints

### Guides
- [ONE_PIECE_TCG_RULES.md](guides/ONE_PIECE_TCG_RULES.md) - Official rules implementation including:
  - Color matching rule
  - Maximum card copies rule
  - Deck size rule
  - Combat rules
  - Testing approach

### Development History
- [IMPROVEMENTS_SUMMARY.md](development/IMPROVEMENTS_SUMMARY.md) - Summary of all improvements
- [REFACTORING_COMPLETE.md](development/REFACTORING_COMPLETE.md) - Refactoring documentation
- [README_STRUCTURE_DECK_FIX.md](development/README_STRUCTURE_DECK_FIX.md) - Structure deck fixes
- [STRUCTURE_DECK_UPDATE_GUIDE.md](development/STRUCTURE_DECK_UPDATE_GUIDE.md) - Update guide

## Contributing to Documentation

When adding or updating documentation:

1. **Location**: Place documentation in the appropriate subdirectory
   - Architecture/design → `architecture/`
   - API/database → `api/`
   - Features → `features/`
   - User/developer guides → `guides/`
   - Development history → `development/`

2. **Format**: Use Markdown (.md) format

3. **Structure**: Include:
   - Clear title and overview
   - Table of contents for long documents
   - Code examples where appropriate
   - Links to related documentation

4. **Naming**: Use descriptive, UPPER_SNAKE_CASE names for consistency

5. **Updates**: Keep documentation in sync with code changes

## Documentation Standards

### Markdown Style
- Use `#` for main title, `##` for sections, `###` for subsections
- Use code blocks with language specification: ```python
- Use bullet points for lists
- Include links to related documents
- Add examples for clarity

### Code Examples
- Keep examples concise and focused
- Include comments explaining non-obvious code
- Show both input and expected output
- Use realistic data

### Maintenance
- Update documentation when features change
- Remove outdated information
- Add new sections for new features
- Keep the documentation structure organized

## Getting Help

If you can't find what you're looking for:

1. Check the [Main README](../README.md) first
2. Browse the relevant subdirectory
3. Search within documentation files
4. Check source code comments
5. Open an issue on the repository

## Related Directories

- [src/](../src/README.md) - Source code
- [tests/](../tests/README.md) - Test suite
- [static/](../static/README.md) - Static assets (CSS, JS)
- [templates/](../templates/README.md) - HTML templates
