# Structure Deck Update Guide

## Overview
This guide explains how to update structure deck data with accurate card lists from the official One Piece TCG website.

## Structure Deck URLs
Card lists for each structure deck can be found at:
- Base URL: `https://en.onepiece-cardgame.com/cardlist/?series=569XXX`
- Where XXX is the structure deck number (e.g., ST-28 = 569028)

### Specific URLs:
- ST-22: https://en.onepiece-cardgame.com/cardlist/?series=569022
- ST-23: https://en.onepiece-cardgame.com/cardlist/?series=569023
- ST-24: https://en.onepiece-cardgame.com/cardlist/?series=569024
- ST-25: https://en.onepiece-cardgame.com/cardlist/?series=569025
- ST-26: https://en.onepiece-cardgame.com/cardlist/?series=569026
- ST-27: https://en.onepiece-cardgame.com/cardlist/?series=569027
- ST-28: https://en.onepiece-cardgame.com/cardlist/?series=569028

## Update Process

### Option 1: Using the Scraper Script
If you have internet access to the official website:

```bash
# Install dependencies
pip install beautifulsoup4 requests

# Run the scraper
python scrape_structure_decks.py

# This will create structure_deck_data.json with the card data
# and print Python code that can be copied into structure_decks.py
```

### Option 2: Manual Update
1. Visit each structure deck URL above
2. Note the deck name, leader, and all cards with their quantities
3. Update the corresponding entry in `structure_decks.py`

## Data Format

Each structure deck entry should follow this format:

```python
'ST-XX': {
    'code': 'ST-XX',
    'name': 'Deck Name',
    'description': 'Deck description',
    'color': 'Primary Color',  # Red, Blue, Green, Purple, Black, or Yellow
    'leader': 'Leader Card Name',
    'cards': {
        'Leader Card Name': 1,  # Leader
        'Card Name 1': 4,       # Quantity
        'Card Name 2': 3,
        # ... more cards
    }
}
```

## Validation

After updating, run the validation tests:

```bash
# Check that all decks have exactly 50 cards
python test_structure_deck_counts.py

# Run full structure deck tests
python test_structure_decks.py
```

## Notes

- Each structure deck must have exactly 50 cards total (including 1 leader)
- Card quantities are typically 1-4 per card (max 4 copies per non-leader card)
- The leader is included in the 'cards' dictionary with quantity 1
- Total cards = sum of all card quantities must equal 50
