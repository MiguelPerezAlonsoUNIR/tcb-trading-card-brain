# TCB Trading Card Brain 🧠 

An AI-powered web application for building optimized decks for Trading Card Games, starting with One Piece TCG.

## Features

- **User Authentication**: Secure user registration and login system
- **Personal Deck Storage**: Save and manage your decks in your user profile
- **Card Collection Tracking**: Track which cards you own for better deck suggestions
- **AI-Powered Deck Building**: Intelligent deck construction based on strategy and color preferences
- **One Piece TCG Rules Enforcement**: Follows official One Piece TCG deck building rules, including color matching
- **Collection-Based Suggestions**: Get deck suggestions based on cards you already own
- **One Piece TCG Support**: Built-in database of One Piece Trading Card Game cards
- **Card Images**: Visual card display with images from official One Piece TCG API
- **Strategy Options**: Choose from Aggressive, Balanced, or Control strategies
- **Color Filtering**: Build decks focused on specific colors or multi-color combinations
- **Deck Analysis**: Get AI-powered insights and suggestions for your deck
- **Interactive Web UI**: Beautiful, responsive interface for deck building
- **Export Functionality**: Export your decks as text files
- **Docker Support**: Easy deployment with Docker containers

## Technology Stack

- **Backend**: Python 3.11 with Flask
- **Authentication**: Flask-Login for session management
- **Database**: SQLAlchemy with SQLite (easily upgradable to PostgreSQL/MySQL)
- **AI Library**: Python-based deck building algorithms (extensible to use ML models)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Containerization**: Docker with multi-stage builds

## Quick Start

### Using Docker (Recommended)

1. Build the Docker image:
```bash
docker build -t onepiece-deck-builder .
```

2. Run the container:
```bash
docker run -p 5000:5000 onepiece-deck-builder
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

### Using Docker Compose

1. Start the application:
```bash
docker-compose up
```

2. Access the application at `http://localhost:5000`

### Manual Installation

1. Install Python 3.11 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set environment variables:
```bash
export SECRET_KEY="your-secret-key-here"  # For production
export DATABASE_URL="sqlite:///tcb.db"     # Default database
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Configuration

The application can be configured using environment variables:

- `SECRET_KEY`: Secret key for session management (default: 'dev-secret-key-change-in-production')
- `DATABASE_URL`: Database connection string (default: 'sqlite:///tcb.db')
- `FLASK_ENV`: Set to 'development' for debug mode

**Important**: For production deployments, always set a strong `SECRET_KEY` and use a production-grade database.

## Usage Guide

### User Authentication

1. **Register an Account**:
   - Click "Register" in the header
   - Choose a username (minimum 3 characters)
   - Create a password (minimum 6 characters)
   - Your account is created and you're automatically logged in

2. **Login to Existing Account**:
   - Click "Login" in the header
   - Enter your username and password
   - Access your saved decks and collection

### Managing Your Card Collection

1. **Add Cards to Collection**:
   - Click "My Collection" in the header (requires login)
   - Click "Add Card to Collection"
   - Enter the card name and quantity you own
   - Track all cards you physically possess

2. **Get Deck Suggestions Based on Your Collection**:
   - Go to "My Collection"
   - Click "Suggest Deck from Collection"
   - The AI will build a deck and show you:
     - What percentage of cards you already own
     - Which cards you need to acquire
     - Optimized deck based on your collection

### Building a Deck

1. **Select Strategy**:
   - **Aggressive**: Focus on low-cost, high-power characters for early pressure
   - **Balanced**: Mix of characters, events, and stages for versatility
   - **Control**: Higher-cost cards with removal and control elements

2. **Choose Color**:
   - Select a primary color (Red, Blue, Green, Purple, Black, Yellow)
   - Or choose "Any" for multi-color decks

3. **Optional Leader Selection**:
   - Specify a leader by name (e.g., "Monkey D. Luffy")
   - Leave empty for automatic leader selection

4. Click "Build Deck" to generate your optimized 50-card deck

**Important Note**: The deck builder follows official One Piece TCG rules:
- All cards in your deck must share at least one color with your leader
- Multi-color leaders (e.g., Trafalgar Law - Blue/Black) allow cards from any of their colors
- Maximum 4 copies of any card (excluding the leader)
- Deck size: 50 cards (some color combinations may have fewer cards due to database limitations)

### Saving Your Decks

After building a deck (requires login):
1. Click "Save Deck"
2. Give your deck a name
3. Access your saved decks anytime from "My Decks"

### Analyzing Your Deck

After building a deck, click "Analyze Deck" to receive:
- Cost curve analysis
- Type distribution breakdown
- Color balance assessment
- AI-powered suggestions for improvement

### Improving Your Deck

After viewing a deck, you can request improvement suggestions:
1. Click "Suggest Improvements" to get three optimized variations:
   - **Balanced Deck**: Optimized for versatile gameplay with 65% characters, 30% events, and 5% stages
   - **Aggressive Deck**: Optimized for early pressure with 75% low-cost characters for fast gameplay
   - **Tournament Deck**: Optimized based on competitive patterns with balanced cost curves proven in tournament play
2. Each suggestion shows:
   - Complete deck list with your chosen leader
   - Description of the improvement strategy
   - Changes from your current deck
   - Collection coverage (if logged in) showing which cards you already own
3. You can save any suggested improvement as a new deck

### Exporting Your Deck

Click "Export Deck" to download your deck list as a text file, perfect for:
- Sharing with friends
- Importing into other tools
- Printing for reference

## Project Structure

The project has been refactored with a modular architecture for better maintainability. See [ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) for detailed documentation.

```
tcb-trading-card-brain/
├── src/                        # Source code package
│   ├── api/                    # API layer (routes, blueprints)
│   │   └── routes/            # Organized route blueprints
│   ├── config/                 # Configuration management
│   ├── core/                   # Constants and utilities
│   ├── models/                 # Database models
│   └── services/               # Business logic layer
├── app.py                      # Application entry point
├── deck_builder.py             # AI deck building logic
├── combat_simulator.py         # Combat simulation
├── structure_decks.py          # Structure deck definitions
├── cards_data.py              # Card database
├── templates/                  # HTML templates
├── static/                     # Static assets (CSS, JS)
├── tests/                      # Test suite
│   ├── unit/                  # Unit tests (no dependencies)
│   └── system/                # System/integration tests
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── docs/                      # Documentation
│   ├── architecture/         # Architecture docs
│   ├── api/                  # API & database docs
│   ├── features/             # Feature documentation
│   ├── guides/               # User & developer guides
│   └── development/          # Development history
└── README.md                  # This file
```

### Architecture Highlights

- **Modular Design**: Code organized into logical packages (api, services, models, config)
- **Service Layer**: Business logic separated from API routes
- **Centralized Configuration**: All settings in one place
- **Blueprint Pattern**: API routes organized by domain
- **Backwards Compatible**: Existing code still works with compatibility wrappers

For details on the architecture, design patterns, and development guidelines, see [ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md).

## API Endpoints

### Authentication Endpoints

#### POST /api/register
Register a new user
```json
{
  "username": "string (min 3 chars)",
  "password": "string (min 6 chars)"
}
```

#### POST /api/login
Login with existing credentials
```json
{
  "username": "string",
  "password": "string"
}
```

#### POST /api/logout
Logout current user (no body required)

#### GET /api/current-user
Check authentication status and get current user info

### Deck Management Endpoints (Requires Authentication)

#### GET /api/decks
Get all decks for the current user

#### POST /api/decks
Save a new deck
```json
{
  "name": "string",
  "strategy": "balanced|aggressive|control",
  "color": "string",
  "leader": {object},
  "main_deck": [array of card objects]
}
```

#### GET /api/decks/:id
Get a specific deck by ID

#### PUT /api/decks/:id
Update a specific deck

#### DELETE /api/decks/:id
Delete a specific deck

### Collection Management Endpoints (Requires Authentication)

#### GET /api/collection
Get user's card collection

#### POST /api/collection
Add or update card in collection
```json
{
  "card_name": "string",
  "quantity": number
}
```

#### DELETE /api/collection/:id
Remove a card from collection

#### POST /api/suggest-deck
Build a deck based on user's collection
```json
{
  "strategy": "balanced|aggressive|control",
  "color": "Red|Blue|Green|Purple|Black|Yellow|any"
}
```

### Public Endpoints

#### GET /
Returns the landing page with TCG selection grid

#### GET /onepiece
Returns the One Piece TCG deck builder interface

#### GET /api/cards
Returns all available One Piece TCG cards with image URLs

#### POST /api/build-deck
Builds a deck based on preferences
```json
{
  "strategy": "balanced|aggressive|control",
  "color": "Red|Blue|Green|Purple|Black|Yellow|any",
  "leader": "optional leader name"
}
```

#### POST /api/analyze-deck
Analyzes a deck and provides suggestions
```json
{
  "deck": [array of card objects]
}
```

#### POST /api/suggest-improvements
Suggests three improved deck variations (balanced, aggressive, tournament-competitive)
```json
{
  "deck": {
    "leader": {leader card object},
    "main_deck": [array of card objects],
    "strategy": "string",
    "color": "string"
  }
}
```

Returns three improved deck variations with:
- Complete deck list for each improvement type
- Description of optimization strategy
- Changes from original deck
- Collection coverage (if authenticated)

## One Piece TCG Rules Compliance

This application follows the official One Piece TCG deck building rules as defined in the [One Piece TCG Rule Manual](https://en.onepiece-cardgame.com/pdf/rule_manual.pdf):

### Deck Construction Rules

1. **Leader Card**: Each deck must have exactly 1 Leader card
2. **Deck Size**: Main deck must contain exactly 50 cards (excluding the Leader)
3. **Card Copies**: Maximum of 4 copies of any single card (Leaders don't count toward this limit)
4. **Color Matching Rule**: All cards in the deck must share at least one color with the Leader
   - Single-color leaders (e.g., Monkey D. Luffy - Red): All cards must include Red in their colors
   - Multi-color leaders (e.g., Trafalgar Law - Blue/Black): Cards can be Blue, Black, or both
   - Multi-color cards are allowed as long as they share at least one color with the leader

### AI Enforcement

The deck builder AI automatically enforces these rules:
- ✓ Cards are filtered to match the leader's colors
- ✓ Maximum 4 copies per card is enforced
- ✓ Deck analysis will warn if deck size is not exactly 50 cards
- ✓ Color validation works for both single and multi-color leaders

**Note**: Some color combinations may result in decks with fewer than 50 cards due to the current card database size. To build full 50-card decks, add more cards to `cards_data.py` that match the desired colors.

## Extending the Application

### Card Database Management

The application uses a database to store all card information, making it easy to add new cards and expansions.

#### Loading Data from Kaggle (Recommended)

The application now supports loading card data from the comprehensive [One Piece TCG Card Database on Kaggle](https://www.kaggle.com/datasets/jbowski/one-piece-tcg-card-database):

```bash
# Download and load data from Kaggle
python load_kaggle_data.py --download
```

This provides:
- Complete card database with all expansions
- Up-to-date card information
- Structure deck definitions
- Community-maintained data

**Setup Requirements:**
1. Install dependencies: `pip install -r requirements.txt`
2. Setup Kaggle API credentials (see [docs/KAGGLE_DATASET.md](docs/KAGGLE_DATASET.md))

For detailed instructions, see [Kaggle Dataset Integration Guide](docs/KAGGLE_DATASET.md).

#### Initializing the Card Database (Legacy)

Alternatively, you can use the legacy initialization script with hardcoded cards:

```bash
python init_cards_db.py
```

This script will:
- Create all necessary database tables
- Import cards from `cards_data.py` into the database
- Set up card sets (expansions)
- Display statistics about the imported cards

#### Adding New Cards via API

You can add new cards using the API endpoints:

**Add a new card:**
```bash
curl -X POST http://localhost:5000/api/admin/cards \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Card Name",
    "type": "Character",
    "colors": ["Red", "Blue"],
    "power": 5000,
    "cost": 4,
    "attribute": "Strike",
    "effect": "Card effect text",
    "set": "OP03",
    "card_number": "025",
    "rarity": "Rare",
    "image_url": "https://example.com/card.png"
  }'
```

**Add a new card set (expansion):**
```bash
curl -X POST http://localhost:5000/api/admin/card-sets \
  -H "Content-Type: application/json" \
  -d '{
    "code": "OP03",
    "name": "Pillars of Strength",
    "release_date": "2024-03-01"
  }'
```

#### Managing Cards

The following admin API endpoints are available for card management:

- `GET /api/admin/cards` - List all cards (with optional filtering by type, color, set)
- `POST /api/admin/cards` - Add a new card
- `PUT /api/admin/cards/<id>` - Update an existing card
- `DELETE /api/admin/cards/<id>` - Delete a card
- `GET /api/admin/card-sets` - List all card sets
- `POST /api/admin/card-sets` - Add a new card set

#### Database Schema

The card database consists of three main tables:

1. **card_sets** - Stores information about card sets/expansions
   - `id`: Primary key
   - `code`: Unique set code (e.g., "OP01", "ST01")
   - `name`: Set name
   - `release_date`: Release date (optional)

2. **cards** - Stores all card information
   - `id`: Primary key
   - `name`: Card name
   - `card_type`: Leader, Character, Event, or Stage
   - `colors`: JSON array of colors
   - `power`, `cost`, `life`: Card stats
   - `attribute`: Strike, Slash, Special, etc.
   - `effect`: Card effect text
   - `set_id`: Foreign key to card_sets
   - `card_number`: Card number within set
   - `rarity`: Common, Rare, Super Rare, etc.
   - `image_url`: URL to card image

3. **user_collections** - Links users to cards they own

### Legacy Card Data

The `cards_data.py` file is still present for backward compatibility and serves as the initial data source. Once the database is initialized, all card data is loaded from the database.

### Adding New TCGs

To support additional Trading Card Games:

1. Create a new card database file (e.g., `pokemon_cards.py`)
2. Implement a new deck builder class
3. Add routing in `app.py` for the new game
4. Update the frontend to support multiple games

### Integrating Machine Learning

The current implementation uses rule-based AI. To add ML capabilities:

1. Install additional ML libraries (e.g., `transformers`, `tensorflow`)
2. Train a model on competitive deck data
3. Replace or augment the deck building logic in `deck_builder.py`
4. Update `requirements.txt` with new dependencies

## Cloud Deployment

The application can be deployed to AWS, Azure, or GCP using Infrastructure as Code (IaC) tools.

### Quick Cloud Deployment

```bash
# Navigate to infrastructure directory
cd infrastructure

# Choose your cloud provider and follow the deployment guide
# See infrastructure/README.md for detailed instructions
```

### Supported Deployment Options

- **AWS**: EC2 instances with optional RDS PostgreSQL
- **Azure**: Virtual Machines with optional Azure Database
- **GCP**: Compute Engine with optional Cloud SQL

### Infrastructure Tools

- **Terraform**: Infrastructure provisioning (AWS, Azure, GCP)
- **Ansible**: Application deployment and configuration
- **Packer**: Pre-built machine images for faster deployments
- **Vagrant**: Local infrastructure testing

### Documentation

- **[Deployment Guide](docs/DEPLOYMENT.md)**: Step-by-step cloud deployment instructions
- **[Infrastructure README](infrastructure/README.md)**: Detailed infrastructure documentation
- **[Infrastructure Analysis](infrastructure/ANALYSIS.md)**: Tool comparison and recommendations

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
python app.py
```

### Local Infrastructure Testing with Vagrant

Test the deployment locally before pushing to cloud:

```bash
cd infrastructure/vagrant
vagrant up

# Access application at:
# - Flask: http://localhost:5000
# - Nginx: http://localhost:8080
```

### Running Tests

```bash
# Add pytest to requirements.txt
pip install pytest
pytest tests/
```

## Contributing

Contributions are welcome! Areas for improvement:

- Additional One Piece TCG cards
- Support for other TCGs (Pokemon, Magic: The Gathering, Yu-Gi-Oh!, etc.)
- Machine learning integration
- Tournament-level deck optimization
- Deck sharing and community features
- Advanced filtering and search
- Card image caching for better performance

## License

This project is open source and available under the MIT License.

## Acknowledgments

- One Piece TCG by Bandai
- Flask framework
- The Python community

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.
