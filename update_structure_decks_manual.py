#!/usr/bin/env python3
"""
Manual structure deck data entry helper
This script helps manually enter structure deck card data
"""

import json
import sys

def input_structure_deck():
    """Interactive prompt to enter structure deck data"""
    print("="*70)
    print("Structure Deck Data Entry")
    print("="*70)
    
    deck_code = input("Enter deck code (e.g., ST-22): ").strip().upper()
    deck_name = input("Enter deck name: ").strip()
    description = input("Enter deck description: ").strip()
    color = input("Enter primary color (Red/Blue/Green/Purple/Black/Yellow): ").strip()
    leader = input("Enter leader card name: ").strip()
    
    print("\nEnter cards (one per line, format: CardName|Quantity)")
    print("Enter 'done' when finished")
    print("Example: Monkey D. Luffy|1")
    
    cards = {}
    while True:
        card_input = input("> ").strip()
        if card_input.lower() == 'done':
            break
        
        try:
            if '|' in card_input:
                name, qty = card_input.rsplit('|', 1)
                cards[name.strip()] = int(qty.strip())
            else:
                print("Invalid format. Use: CardName|Quantity")
        except ValueError:
            print("Invalid quantity. Please enter a number.")
    
    total_cards = sum(cards.values())
    print(f"\nTotal cards: {total_cards}")
    
    if total_cards != 50:
        print(f"WARNING: Structure decks should have exactly 50 cards, you have {total_cards}")
        cont = input("Continue anyway? (y/n): ")
        if cont.lower() != 'y':
            return None
    
    deck_data = {
        'code': deck_code,
        'name': deck_name,
        'description': description,
        'color': color,
        'leader': leader,
        'cards': cards
    }
    
    return deck_data

def format_for_python(deck_data):
    """Format deck data as Python code for structure_decks.py"""
    code = deck_data['code']
    
    output = f"    '{code}': {{\n"
    output += f"        'code': '{code}',\n"
    output += f"        'name': '{deck_data['name']}',\n"
    output += f"        'description': '{deck_data['description']}',\n"
    output += f"        'color': '{deck_data['color']}',\n"
    output += f"        'leader': '{deck_data['leader']}',\n"
    output += f"        'cards': {{\n"
    
    for card_name, quantity in sorted(deck_data['cards'].items()):
        output += f"            '{card_name}': {quantity},\n"
    
    output += f"        }}\n"
    output += f"    }},\n"
    
    return output

def main():
    """Main function"""
    decks = []
    
    while True:
        deck = input_structure_deck()
        if deck:
            decks.append(deck)
            print(f"\n✓ Added {deck['code']}")
            
            another = input("\nAdd another deck? (y/n): ")
            if another.lower() != 'y':
                break
        else:
            break
    
    if not decks:
        print("No decks entered.")
        return 1
    
    # Save to JSON
    with open('manual_structure_decks.json', 'w') as f:
        json.dump(decks, f, indent=2)
    
    print("\n" + "="*70)
    print("Python code for structure_decks.py:")
    print("="*70)
    
    for deck in decks:
        print(format_for_python(deck))
    
    print("="*70)
    print(f"\nData saved to: manual_structure_decks.json")
    print(f"Total decks entered: {len(decks)}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
