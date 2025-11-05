#!/usr/bin/env python
"""
Initialize the card database with cards from cards_data.py
This script migrates the hardcoded card data to the database
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Card, CardSet
from cards_data import ONEPIECE_CARDS
from datetime import datetime

def init_card_sets():
    """Initialize card sets from the cards data"""
    print("Initializing card sets...")
    
    # Extract unique sets from cards
    sets_data = {}
    for card in ONEPIECE_CARDS:
        set_code = card.get('set')
        if set_code and set_code not in sets_data:
            # Map set codes to names
            set_names = {
                'ST01': 'Straw Hat Crew Starter Deck',
                'ST02': 'Worst Generation Starter Deck',
                'ST03': 'The Seven Warlords of the Sea Starter Deck',
                'ST04': 'Animal Kingdom Pirates Starter Deck',
                'OP01': 'Romance Dawn',
                'OP02': 'Paramount War',
            }
            set_name = set_names.get(set_code, f'Set {set_code}')
            sets_data[set_code] = set_name
    
    # Create card sets in database
    set_id_map = {}
    for set_code, set_name in sets_data.items():
        # Check if set already exists
        card_set = CardSet.query.filter_by(code=set_code).first()
        if not card_set:
            card_set = CardSet(
                code=set_code,
                name=set_name,
                release_date=None  # Could be added later
            )
            db.session.add(card_set)
            db.session.flush()  # Flush to get the ID
        set_id_map[set_code] = card_set.id
        print(f"  ✓ Card Set: {set_code} - {set_name}")
    
    db.session.commit()
    return set_id_map

def init_cards(set_id_map):
    """Initialize cards from cards_data.py"""
    print("\nInitializing cards...")
    
    cards_added = 0
    cards_skipped = 0
    
    for card_data in ONEPIECE_CARDS:
        set_code = card_data.get('set')
        card_number = card_data.get('card_number')
        
        if not set_code or not card_number:
            print(f"  ⚠ Skipping card {card_data.get('name', 'Unknown')} - missing set or card_number")
            cards_skipped += 1
            continue
        
        set_id = set_id_map.get(set_code)
        if not set_id:
            print(f"  ⚠ Skipping card {card_data.get('name', 'Unknown')} - set {set_code} not found")
            cards_skipped += 1
            continue
        
        # Check if card already exists
        existing_card = Card.query.filter_by(set_id=set_id, card_number=card_number).first()
        if existing_card:
            cards_skipped += 1
            continue
        
        # Create new card
        card = Card(
            name=card_data.get('name', ''),
            card_type=card_data.get('type', ''),
            power=card_data.get('power'),
            cost=card_data.get('cost', 0),
            life=card_data.get('life'),
            attribute=card_data.get('attribute'),
            effect=card_data.get('effect'),
            set_id=set_id,
            card_number=card_number,
            rarity=card_data.get('rarity'),
            image_url=card_data.get('image_url')
        )
        
        # Set colors as JSON
        colors = card_data.get('colors', [])
        card.set_colors(colors)
        
        db.session.add(card)
        cards_added += 1
        
        if cards_added % 10 == 0:
            print(f"  ... {cards_added} cards added")
    
    db.session.commit()
    print(f"\n✓ Successfully added {cards_added} cards")
    if cards_skipped > 0:
        print(f"  (Skipped {cards_skipped} cards - already exist or invalid data)")

def main():
    """Main initialization function"""
    print("=" * 60)
    print("Card Database Initialization")
    print("=" * 60)
    
    with app.app_context():
        # Create all tables
        print("\nCreating database tables...")
        db.create_all()
        print("✓ Tables created")
        
        # Initialize card sets
        set_id_map = init_card_sets()
        
        # Initialize cards
        init_cards(set_id_map)
        
        # Print summary
        print("\n" + "=" * 60)
        print("Database Initialization Complete")
        print("=" * 60)
        
        total_sets = CardSet.query.count()
        total_cards = Card.query.count()
        total_leaders = Card.query.filter_by(card_type='Leader').count()
        total_characters = Card.query.filter_by(card_type='Character').count()
        total_events = Card.query.filter_by(card_type='Event').count()
        total_stages = Card.query.filter_by(card_type='Stage').count()
        
        print(f"\nDatabase Statistics:")
        print(f"  Total Card Sets: {total_sets}")
        print(f"  Total Cards: {total_cards}")
        print(f"    - Leaders: {total_leaders}")
        print(f"    - Characters: {total_characters}")
        print(f"    - Events: {total_events}")
        print(f"    - Stages: {total_stages}")
        print("\n✓ Ready to use!")

if __name__ == '__main__':
    main()
