#!/usr/bin/env python3
"""
Demonstration script showing how the Lorcana card scraper integrates with
the TCB Trading Card Brain application.

This script shows:
1. How to fetch cards from dreamborn.ink
2. How to integrate with the Lorcana deck builder
3. How to use the cards in deck building

Note: This is a demonstration. In production, you would run the scraper
separately and load the JSON file at runtime.
"""

import sys
import json
from typing import List, Dict


def demo_scraper_usage():
    """Demonstrate using the Lorcana card scraper"""
    print("="*70)
    print("Lorcana Card Scraper - Integration Demonstration")
    print("="*70)
    print()
    
    # Import the scraper
    try:
        from scrape_lorcana_cards import LorcanaCardScraper
    except ImportError:
        print("Error: Cannot import scraper. Make sure scrape_lorcana_cards.py is in the same directory.")
        return 1
    
    # Step 1: Create scraper instance
    print("Step 1: Creating scraper instance...")
    scraper = LorcanaCardScraper(verbose=True)
    print()
    
    # Step 2: Test connectivity
    print("Step 2: Testing connectivity to dreamborn.ink...")
    if not scraper.test_connectivity():
        print("\n⚠️  dreamborn.ink is not accessible from this environment.")
        print("This is expected in restricted networks.")
        print("\nIn a real scenario, you would:")
        print("  1. Run this script on a machine with internet access")
        print("  2. Generate the lorcana_cards.json file")
        print("  3. Commit the JSON file to your repository")
        print("  4. Load cards from the JSON file in your application")
        print()
        demo_with_sample_data()
        return 0
    
    # Step 3: Fetch cards (this will only work if dreamborn.ink is accessible)
    print("\nStep 3: Fetching cards from dreamborn.ink...")
    cards = scraper.fetch_all_cards()
    
    if not cards:
        print("Failed to fetch cards. Using sample data instead.")
        demo_with_sample_data()
        return 0
    
    print(f"✓ Successfully fetched {len(cards)} cards")
    print()
    
    # Step 4: Save to file
    print("Step 4: Saving cards to lorcana_cards_demo.json...")
    scraper.save_cards(cards, 'lorcana_cards_demo.json')
    print()
    
    # Step 5: Demonstrate integration
    print("Step 5: Demonstrating deck building with fetched cards...")
    demo_deck_building(cards)
    
    return 0


def demo_with_sample_data():
    """Demonstrate with sample Lorcana cards"""
    print("\n" + "="*70)
    print("Using Sample Card Data")
    print("="*70)
    print()
    
    # Sample cards (matching the format from scraper)
    sample_cards = [
        {
            'name': 'Simba - Protective Cub',
            'type': 'Character',
            'colors': ['Amber'],
            'cost': 1,
            'power': 1,
            'effect': 'Challenger +2',
            'inkable': True,
            'set': 'TFC',
            'card_number': '123',
            'rarity': 'Common'
        },
        {
            'name': 'Maleficent - Monstrous Dragon',
            'type': 'Character',
            'colors': ['Amethyst'],
            'cost': 8,
            'power': 6,
            'effect': 'Dragon Fire',
            'inkable': True,
            'set': 'TFC',
            'card_number': '234',
            'rarity': 'Legendary'
        },
        {
            'name': 'Elsa - Spirit of Winter',
            'type': 'Character',
            'colors': ['Sapphire'],
            'cost': 5,
            'power': 4,
            'effect': 'Deep Freeze',
            'inkable': True,
            'set': 'TFC',
            'card_number': '345',
            'rarity': 'Rare'
        },
        {
            'name': 'Be Prepared',
            'type': 'Action',
            'colors': ['Amethyst'],
            'cost': 2,
            'effect': 'Draw 2 cards',
            'inkable': True,
            'set': 'TFC',
            'card_number': '456',
            'rarity': 'Common'
        }
    ]
    
    print(f"Sample dataset contains {len(sample_cards)} cards")
    print()
    
    demo_deck_building(sample_cards)


def demo_deck_building(cards: List[Dict]):
    """Demonstrate deck building with Lorcana cards"""
    print("\n" + "="*70)
    print("Deck Building Demonstration")
    print("="*70)
    print()
    
    # Import the Lorcana deck builder
    try:
        from lorcana_deck_builder import LorcanaDeckBuilder
    except ImportError:
        print("Error: Cannot import LorcanaDeckBuilder")
        print("Make sure lorcana_deck_builder.py is in the same directory.")
        return
    
    # Create deck builder instance
    print("Creating Lorcana deck builder...")
    builder = LorcanaDeckBuilder()
    print()
    
    # Show card statistics
    print("Card Statistics:")
    print(f"  Total cards: {len(cards)}")
    
    # Count by type
    types = {}
    for card in cards:
        card_type = card.get('type', 'Unknown')
        types[card_type] = types.get(card_type, 0) + 1
    
    print("  Card types:")
    for card_type, count in sorted(types.items()):
        print(f"    {card_type}: {count}")
    
    # Count by color
    colors = {}
    for card in cards:
        for color in card.get('colors', []):
            colors[color] = colors.get(color, 0) + 1
    
    if colors:
        print("  Card colors:")
        for color, count in sorted(colors.items()):
            print(f"    {color}: {count}")
    
    print()
    
    # Demonstrate deck building (would require full card database)
    print("In a production environment, you would:")
    print("  1. Load all cards from lorcana_cards.json")
    print("  2. Store them in the database using init_cards_db.py pattern")
    print("  3. Build decks using LorcanaDeckBuilder.build_deck()")
    print("  4. Display cards with images from image_url field")
    print()
    
    # Show example card structure
    if cards:
        print("Example card structure:")
        print(json.dumps(cards[0], indent=2))
    
    print()


def main():
    """Main entry point"""
    try:
        return demo_scraper_usage()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
