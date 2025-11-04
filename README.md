# TCB Trading Card Brain 🏴‍☠️

An AI-powered web application for building optimized decks for Trading Card Games, starting with One Piece TCG.

## Features

- **AI-Powered Deck Building**: Intelligent deck construction based on strategy and color preferences
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

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage Guide

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

### Analyzing Your Deck

After building a deck, click "Analyze Deck" to receive:
- Cost curve analysis
- Type distribution breakdown
- Color balance assessment
- AI-powered suggestions for improvement

### Exporting Your Deck

Click "Export Deck" to download your deck list as a text file, perfect for:
- Sharing with friends
- Importing into other tools
- Printing for reference

## Project Structure

```
tcb-trading-card-brain/
├── app.py                  # Flask web application
├── deck_builder.py         # AI deck building logic
├── cards_data.py           # One Piece TCG card database
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── app.js        # Frontend JavaScript
└── README.md             # This file
```

## API Endpoints

### GET /
Returns the main application interface

### GET /api/cards
Returns all available One Piece TCG cards with image URLs
```json
[
  {
    "name": "Monkey D. Luffy",
    "type": "Leader",
    "colors": ["Red"],
    "power": 5000,
    "cost": 0,
    "image_url": "https://en.onepiece-cardgame.com/images/cardlist/ST01-001.png",
    ...
  }
]
```

### POST /api/build-deck
Builds a deck based on preferences
```json
{
  "strategy": "balanced|aggressive|control",
  "color": "Red|Blue|Green|Purple|Black|Yellow|any",
  "leader": "optional leader name"
}
```

### POST /api/analyze-deck
Analyzes a deck and provides suggestions
```json
{
  "deck": [array of card objects]
}
```

## Extending the Application

### Adding More Cards

Edit `cards_data.py` and add card objects to the `ONEPIECE_CARDS` list:

```python
{
    'name': 'Card Name',
    'type': 'Character|Event|Stage|Leader',
    'colors': ['Red'],
    'power': 5000,
    'cost': 4,
    'effect': 'Card effect text',
    'set': 'OP01',
    'card_number': '025',
    'rarity': 'Common|Rare|Super Rare|Secret Rare',
    'image_url': get_card_image_url('OP01', '025')
}
```

The `get_card_image_url()` function automatically generates the correct image URL based on the card set and number.

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

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
python app.py
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