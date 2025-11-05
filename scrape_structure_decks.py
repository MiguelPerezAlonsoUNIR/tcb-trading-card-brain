#!/usr/bin/env python3
"""
Scraper to fetch structure deck card lists from the official One Piece TCG website.
This script fetches card data from https://en.onepiece-cardgame.com/cardlist/?series=569XXX
where XXX corresponds to the structure deck number (e.g., ST-28 = 569028).
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import sys

# Structure deck codes to fetch
STRUCTURE_DECK_CODES = [
    'ST-22', 'ST-23', 'ST-24', 'ST-25', 'ST-26', 'ST-27', 'ST-28'
]

def get_series_number(deck_code):
    """Convert deck code like ST-22 to series number like 569022"""
    deck_num = int(deck_code.split('-')[1])
    return 569000 + deck_num

def fetch_structure_deck_cards(deck_code):
    """
    Fetch card list for a structure deck from the official website
    
    Args:
        deck_code: Structure deck code (e.g., 'ST-22')
    
    Returns:
        Dictionary with deck info and card list, or None if fetch fails
    """
    series_number = get_series_number(deck_code)
    url = f'https://en.onepiece-cardgame.com/cardlist/?series={series_number}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"Fetching {deck_code} from {url}...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find deck name/title
        deck_name = soup.find('h1', class_='pageTitle')
        deck_name_text = deck_name.text.strip() if deck_name else f'Structure Deck {deck_code}'
        
        # Find all card elements
        cards = []
        card_elements = soup.find_all('div', class_='modalCol')
        
        for card_elem in card_elements:
            try:
                # Extract card name
                name_elem = card_elem.find('div', class_='cardName')
                if not name_elem:
                    continue
                card_name = name_elem.text.strip()
                
                # Extract card number and rarity
                num_elem = card_elem.find('div', class_='cardNumber')
                card_number = num_elem.text.strip() if num_elem else ''
                
                # Extract card type
                type_elem = card_elem.find('div', class_='cardType')
                card_type = type_elem.text.strip() if type_elem else ''
                
                # Extract cost
                cost_elem = card_elem.find('div', class_='cardCost')
                cost = cost_elem.text.strip() if cost_elem else ''
                
                # Extract power
                power_elem = card_elem.find('div', class_='cardPower')
                power = power_elem.text.strip() if power_elem else ''
                
                # Extract colors
                color_elem = card_elem.find('div', class_='cardColor')
                colors = color_elem.text.strip() if color_elem else ''
                
                cards.append({
                    'name': card_name,
                    'card_number': card_number,
                    'type': card_type,
                    'cost': cost,
                    'power': power,
                    'colors': colors
                })
            except Exception as e:
                print(f"  Warning: Error parsing card element: {e}")
                continue
        
        if not cards:
            print(f"  Warning: No cards found for {deck_code}")
            return None
        
        # Count card quantities (structure decks typically have specific quantities per card)
        card_counts = {}
        for card in cards:
            name = card['name']
            card_counts[name] = card_counts.get(name, 0) + 1
        
        print(f"  Found {len(cards)} card entries ({len(card_counts)} unique cards)")
        
        # Determine leader (usually the first Leader type card)
        leader = None
        for card in cards:
            if card['type'].lower() == 'leader':
                leader = card['name']
                break
        
        # Determine primary color
        color_counts = {}
        for card in cards:
            if card['colors']:
                for color in card['colors'].split('/'):
                    color = color.strip()
                    color_counts[color] = color_counts.get(color, 0) + 1
        primary_color = max(color_counts, key=color_counts.get) if color_counts else 'Red'
        
        return {
            'code': deck_code,
            'name': deck_name_text,
            'description': f'Official {deck_code} structure deck',
            'color': primary_color,
            'leader': leader or 'Unknown',
            'cards': card_counts,
            'url': url
        }
        
    except requests.RequestException as e:
        print(f"  Error fetching {deck_code}: {e}")
        return None
    except Exception as e:
        print(f"  Error parsing {deck_code}: {e}")
        return None

def main():
    """Main function to scrape all structure decks"""
    print("="*70)
    print("One Piece TCG Structure Deck Scraper")
    print("="*70)
    
    results = {}
    failed = []
    
    for deck_code in STRUCTURE_DECK_CODES:
        deck_data = fetch_structure_deck_cards(deck_code)
        
        if deck_data:
            results[deck_code] = deck_data
            print(f"✓ Successfully fetched {deck_code}")
            
            # Calculate total cards
            total_cards = sum(deck_data['cards'].values())
            print(f"  Total cards: {total_cards}")
            print(f"  Leader: {deck_data['leader']}")
            print(f"  Primary color: {deck_data['color']}")
        else:
            failed.append(deck_code)
            print(f"✗ Failed to fetch {deck_code}")
        
        # Be nice to the server
        time.sleep(2)
        print()
    
    # Save results to JSON file
    output_file = 'structure_deck_data.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("="*70)
    print(f"Scraping complete!")
    print(f"Successfully fetched: {len(results)}/{len(STRUCTURE_DECK_CODES)} decks")
    if failed:
        print(f"Failed to fetch: {', '.join(failed)}")
    print(f"Results saved to: {output_file}")
    print("="*70)
    
    # Generate Python code for structure_decks.py
    if results:
        print("\nGenerated Python code for structure_decks.py:")
        print("-"*70)
        for deck_code, deck_data in sorted(results.items()):
            print(f"    '{deck_code}': {{")
            print(f"        'code': '{deck_code}',")
            print(f"        'name': '{deck_data['name']}',")
            print(f"        'description': '{deck_data['description']}',")
            print(f"        'color': '{deck_data['color']}',")
            print(f"        'leader': '{deck_data['leader']}',")
            print(f"        'cards': {{")
            for card_name, quantity in sorted(deck_data['cards'].items()):
                print(f"            '{card_name}': {quantity},")
            print(f"        }}")
            print(f"    }},")
        print("-"*70)
    
    return 0 if not failed else 1

if __name__ == '__main__':
    try:
        # Check if BeautifulSoup is available
        import bs4
    except ImportError:
        print("Error: BeautifulSoup4 is required. Install it with:")
        print("  pip install beautifulsoup4")
        sys.exit(1)
    
    sys.exit(main())
