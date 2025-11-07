#!/usr/bin/env python3
"""
Scraper to fetch Lorcana card lists from https://dreamborn.ink/es/cards
This script fetches card data and images for Disney Lorcana TCG.

Dreamborn.ink is a community-driven Lorcana card database that provides:
- Card information (name, type, cost, power, etc.)
- Card images
- Card text and effects
- Set information

Note: This script requires network access to dreamborn.ink. If the domain is blocked,
it will provide instructions for manual data retrieval.
"""

import sys
import json
import time
import argparse
from typing import Dict, List, Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Error: Required library not found: {e}")
    print("Install dependencies with: pip install beautifulsoup4 requests")
    sys.exit(1)


class LorcanaCardScraper:
    """Scraper for Lorcana cards from dreamborn.ink"""
    
    BASE_URL = "https://dreamborn.ink"
    CARDS_URL = f"{BASE_URL}/es/cards"
    API_URL = f"{BASE_URL}/api/cards"  # Potential API endpoint
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es,en-US;q=0.7,en;q=0.3',
        })
    
    def log(self, message: str):
        """Print message if verbose mode is enabled"""
        if self.verbose:
            print(message)
    
    def test_connectivity(self) -> bool:
        """Test if dreamborn.ink is accessible"""
        try:
            self.log(f"Testing connectivity to {self.BASE_URL}...")
            response = self.session.get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            self.log(f"✓ Successfully connected to {self.BASE_URL}")
            return True
        except requests.exceptions.ConnectionError as e:
            self.log(f"✗ Connection error: {e}")
            self.log("\nThe domain dreamborn.ink appears to be blocked or inaccessible.")
            self.log("This may be due to network restrictions in your environment.")
            return False
        except requests.exceptions.RequestException as e:
            self.log(f"✗ Request error: {e}")
            return False
    
    def fetch_cards_api(self) -> Optional[List[Dict]]:
        """
        Try to fetch cards from the API endpoint (if available)
        
        Many modern card databases provide a JSON API for easier data access.
        """
        try:
            self.log(f"\nAttempting to fetch from API: {self.API_URL}")
            response = self.session.get(self.API_URL, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            self.log(f"✓ Successfully fetched data from API")
            
            # Parse the API response
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'cards' in data:
                return data['cards']
            else:
                self.log("Warning: Unexpected API response format")
                return None
                
        except requests.exceptions.RequestException as e:
            self.log(f"API fetch failed: {e}")
            return None
        except json.JSONDecodeError as e:
            self.log(f"Failed to parse API response: {e}")
            return None
    
    def fetch_cards_html(self) -> Optional[List[Dict]]:
        """
        Fetch cards by scraping the HTML page
        
        This is a fallback method if the API is not available.
        """
        try:
            self.log(f"\nAttempting to scrape HTML: {self.CARDS_URL}")
            response = self.session.get(self.CARDS_URL, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            self.log(f"✓ Successfully fetched HTML page")
            
            # Parse the HTML to extract card data
            cards = self._parse_card_list(soup)
            
            if cards:
                self.log(f"✓ Successfully parsed {len(cards)} cards from HTML")
                return cards
            else:
                self.log("Warning: No cards found in HTML")
                return None
                
        except requests.exceptions.RequestException as e:
            self.log(f"HTML scraping failed: {e}")
            return None
    
    def _parse_card_list(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parse the card list from HTML soup
        
        Note: This is a template method. The actual CSS selectors need to be
        adjusted based on the real structure of dreamborn.ink website.
        """
        cards = []
        
        # Common patterns for card database websites:
        # - Cards might be in a table with class 'card-list' or 'cards-table'
        # - Each card might be a div with class 'card' or 'card-item'
        # - Card data might be in data-* attributes or specific child elements
        
        # Try multiple common patterns
        card_elements = (
            soup.find_all('div', class_='card') or
            soup.find_all('div', class_='card-item') or
            soup.find_all('tr', class_='card-row') or
            soup.find_all('article', class_='card')
        )
        
        if not card_elements:
            # Try to find any container with card data
            card_elements = soup.find_all(attrs={'data-card-name': True})
        
        for elem in card_elements:
            try:
                card = self._parse_card_element(elem)
                if card:
                    cards.append(card)
            except Exception as e:
                self.log(f"Warning: Failed to parse card element: {e}")
                continue
        
        return cards
    
    def _parse_card_element(self, element) -> Optional[Dict]:
        """
        Parse a single card element from HTML
        
        Note: This needs to be customized based on actual HTML structure
        """
        card = {}
        
        # Try to extract card name
        name_elem = (
            element.find(class_='card-name') or
            element.find(class_='name') or
            element.get('data-card-name')
        )
        if name_elem:
            card['name'] = name_elem.text.strip() if hasattr(name_elem, 'text') else str(name_elem)
        
        # Try to extract card type
        type_elem = element.find(class_='card-type') or element.get('data-card-type')
        if type_elem:
            card['type'] = type_elem.text.strip() if hasattr(type_elem, 'text') else str(type_elem)
        
        # Try to extract ink color
        color_elem = element.find(class_='card-color') or element.get('data-color')
        if color_elem:
            colors_text = color_elem.text.strip() if hasattr(color_elem, 'text') else str(color_elem)
            card['colors'] = [c.strip() for c in colors_text.split(',')]
        
        # Try to extract cost
        cost_elem = element.find(class_='card-cost') or element.get('data-cost')
        if cost_elem:
            cost_text = cost_elem.text.strip() if hasattr(cost_elem, 'text') else str(cost_elem)
            try:
                card['cost'] = int(cost_text)
            except (ValueError, TypeError):
                card['cost'] = 0
        
        # Try to extract power
        power_elem = element.find(class_='card-power') or element.get('data-power')
        if power_elem:
            power_text = power_elem.text.strip() if hasattr(power_elem, 'text') else str(power_elem)
            try:
                card['power'] = int(power_text)
            except (ValueError, TypeError):
                pass
        
        # Try to extract effect/text
        effect_elem = element.find(class_='card-effect') or element.find(class_='card-text')
        if effect_elem:
            card['effect'] = effect_elem.text.strip()
        
        # Try to extract image URL
        img_elem = element.find('img')
        if img_elem and img_elem.get('src'):
            img_url = img_elem['src']
            if not img_url.startswith('http'):
                img_url = f"{self.BASE_URL}{img_url}"
            card['image_url'] = img_url
        
        # Try to extract set information
        set_elem = element.find(class_='card-set') or element.get('data-set')
        if set_elem:
            card['set'] = set_elem.text.strip() if hasattr(set_elem, 'text') else str(set_elem)
        
        # Try to extract card number
        number_elem = element.find(class_='card-number') or element.get('data-number')
        if number_elem:
            card['card_number'] = number_elem.text.strip() if hasattr(number_elem, 'text') else str(number_elem)
        
        # Try to extract rarity
        rarity_elem = element.find(class_='card-rarity') or element.get('data-rarity')
        if rarity_elem:
            card['rarity'] = rarity_elem.text.strip() if hasattr(rarity_elem, 'text') else str(rarity_elem)
        
        # Try to extract inkable status
        inkable_elem = element.find(class_='inkable') or element.get('data-inkable')
        if inkable_elem:
            inkable_text = inkable_elem.text.strip() if hasattr(inkable_elem, 'text') else str(inkable_elem)
            card['inkable'] = inkable_text.lower() in ['true', 'yes', '1', 'inkable']
        
        # Only return card if we got at least a name
        return card if 'name' in card else None
    
    def fetch_all_cards(self) -> Optional[List[Dict]]:
        """
        Fetch all Lorcana cards using the best available method
        
        Returns:
            List of card dictionaries, or None if fetch fails
        """
        # First test connectivity
        if not self.test_connectivity():
            self._show_manual_instructions()
            return None
        
        # Try API first (faster and more reliable)
        cards = self.fetch_cards_api()
        
        # Fall back to HTML scraping if API fails
        if not cards:
            self.log("\nAPI method failed, trying HTML scraping...")
            cards = self.fetch_cards_html()
        
        return cards
    
    def _show_manual_instructions(self):
        """Show instructions for manual data retrieval"""
        print("\n" + "="*70)
        print("MANUAL DATA RETRIEVAL INSTRUCTIONS")
        print("="*70)
        print("\nSince automatic scraping is not possible, you can manually retrieve")
        print("Lorcana card data using one of these methods:")
        print("\n1. Use a browser with network access:")
        print(f"   - Visit: {self.CARDS_URL}")
        print("   - Open browser DevTools (F12)")
        print("   - Look for API calls in the Network tab")
        print("   - Export the JSON data")
        print("\n2. Use an alternative Lorcana API:")
        print("   - lorcast.com API")
        print("   - lorcana-api.com")
        print("   - Other community databases")
        print("\n3. Run this script from a different environment:")
        print("   - Local machine with internet access")
        print("   - Cloud VM with unrestricted network")
        print("   - Container with proper network configuration")
        print("\n4. Check if dreamborn.ink provides:")
        print("   - Official API documentation")
        print("   - Data export/download feature")
        print("   - GitHub repository with card data")
        print("="*70)
    
    def save_cards(self, cards: List[Dict], output_file: str = 'lorcana_cards.json'):
        """Save cards to JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(cards, f, indent=2, ensure_ascii=False)
            self.log(f"\n✓ Saved {len(cards)} cards to {output_file}")
            return True
        except Exception as e:
            self.log(f"\n✗ Failed to save cards: {e}")
            return False
    
    def generate_python_code(self, cards: List[Dict]):
        """Generate Python code for lorcana_deck_builder.py"""
        print("\n" + "="*70)
        print("GENERATED PYTHON CODE FOR lorcana_deck_builder.py")
        print("="*70)
        print("\nAdd this to the _get_sample_lorcana_cards() method:")
        print("-"*70)
        print("sample_cards = [")
        
        for card in cards[:50]:  # Limit to first 50 cards for readability
            print(f"    {{")
            print(f"        'name': {repr(card.get('name', 'Unknown'))},")
            print(f"        'type': {repr(card.get('type', 'Character'))},")
            print(f"        'colors': {repr(card.get('colors', ['Amber']))},")
            print(f"        'cost': {card.get('cost', 0)},")
            if 'power' in card:
                print(f"        'power': {card.get('power')},")
            if 'effect' in card:
                print(f"        'effect': {repr(card.get('effect', ''))},")
            if 'inkable' in card:
                print(f"        'inkable': {card.get('inkable', True)},")
            if 'set' in card:
                print(f"        'set': {repr(card.get('set', 'TFC'))},")
            if 'card_number' in card:
                print(f"        'card_number': {repr(card.get('card_number', ''))},")
            if 'rarity' in card:
                print(f"        'rarity': {repr(card.get('rarity', 'Common'))},")
            if 'image_url' in card:
                print(f"        'image_url': {repr(card.get('image_url'))},")
            print(f"    }},")
        
        if len(cards) > 50:
            print(f"    # ... and {len(cards) - 50} more cards")
        
        print("]")
        print("-"*70)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Scrape Lorcana cards from dreamborn.ink',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch all cards and save to default file
  python scrape_lorcana_cards.py

  # Fetch cards and save to specific file
  python scrape_lorcana_cards.py --output my_cards.json

  # Run in quiet mode
  python scrape_lorcana_cards.py --quiet

  # Generate Python code only (no file save)
  python scrape_lorcana_cards.py --generate-code
        """
    )
    
    parser.add_argument(
        '-o', '--output',
        default='lorcana_cards.json',
        help='Output JSON file (default: lorcana_cards.json)'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )
    
    parser.add_argument(
        '-g', '--generate-code',
        action='store_true',
        help='Generate Python code for lorcana_deck_builder.py'
    )
    
    parser.add_argument(
        '--test-connectivity',
        action='store_true',
        help='Only test connectivity to dreamborn.ink'
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("Lorcana Card Scraper - dreamborn.ink")
    print("="*70)
    
    scraper = LorcanaCardScraper(verbose=not args.quiet)
    
    # Just test connectivity if requested
    if args.test_connectivity:
        result = scraper.test_connectivity()
        return 0 if result else 1
    
    # Fetch cards
    cards = scraper.fetch_all_cards()
    
    if not cards:
        print("\n✗ Failed to fetch cards from dreamborn.ink")
        print("See the manual instructions above for alternative methods.")
        return 1
    
    print(f"\n✓ Successfully fetched {len(cards)} cards")
    
    # Show statistics
    print("\nCard Statistics:")
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
    
    # Save to file
    if not args.generate_code:
        scraper.save_cards(cards, args.output)
    
    # Generate Python code if requested
    if args.generate_code and cards:
        scraper.generate_python_code(cards)
    
    print("\n" + "="*70)
    print("Scraping complete!")
    print("="*70)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
