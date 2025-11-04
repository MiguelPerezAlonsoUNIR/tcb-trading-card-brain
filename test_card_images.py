#!/usr/bin/env python
"""
Test script to verify card image URLs are properly set
"""

from deck_builder import OnePieceDeckBuilder
from cards_data import ONEPIECE_CARDS

def test_card_images():
    """Test that all cards have image URLs"""
    print("=" * 60)
    print("Card Image URL Test Suite")
    print("=" * 60)
    
    builder = OnePieceDeckBuilder()
    cards = builder.get_all_cards()
    
    # Test 1: Check all cards have image_url field
    print("\nTest 1: Verifying all cards have image_url field")
    cards_without_images = []
    for card in cards:
        if 'image_url' not in card:
            cards_without_images.append(card['name'])
    
    if cards_without_images:
        print(f"✗ {len(cards_without_images)} cards missing image_url:")
        for name in cards_without_images:
            print(f"  - {name}")
    else:
        print(f"✓ All {len(cards)} cards have image_url field")
    
    # Test 2: Check all cards have card_number field
    print("\nTest 2: Verifying all cards have card_number field")
    cards_without_numbers = []
    for card in cards:
        if 'card_number' not in card:
            cards_without_numbers.append(card['name'])
    
    if cards_without_numbers:
        print(f"✗ {len(cards_without_numbers)} cards missing card_number:")
        for name in cards_without_numbers:
            print(f"  - {name}")
    else:
        print(f"✓ All {len(cards)} cards have card_number field")
    
    # Test 3: Check image URLs are properly formatted
    print("\nTest 3: Verifying image URL format")
    invalid_urls = []
    for card in cards:
        url = card.get('image_url', '')
        if not url.startswith('https://') or not url.endswith('.png'):
            invalid_urls.append(f"{card['name']}: {url}")
    
    if invalid_urls:
        print(f"✗ {len(invalid_urls)} cards have invalid image URLs:")
        for info in invalid_urls:
            print(f"  - {info}")
    else:
        print(f"✓ All image URLs are properly formatted")
    
    # Test 4: Sample image URLs
    print("\nTest 4: Sample image URLs")
    print("-" * 60)
    sample_cards = [card for card in cards if card['type'] == 'Leader'][:3]
    for card in sample_cards:
        print(f"{card['name']}:")
        print(f"  Set: {card['set']}, Number: {card['card_number']}")
        print(f"  URL: {card['image_url']}")
    
    # Test 5: Build deck and verify image URLs are passed through
    print("\n" + "-" * 60)
    print("Test 5: Verifying deck building includes image URLs")
    print("-" * 60)
    deck = builder.build_deck(strategy='balanced', color='Red')
    
    # Check leader has image_url
    if 'image_url' in deck['leader']:
        print(f"✓ Leader card has image_url: {deck['leader']['name']}")
    else:
        print(f"✗ Leader card missing image_url")
    
    # Check main deck cards have image_url
    cards_with_images = sum(1 for card in deck['main_deck'] if 'image_url' in card)
    print(f"✓ {cards_with_images}/{len(deck['main_deck'])} main deck cards have image_url")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    if not cards_without_images and not cards_without_numbers and not invalid_urls:
        print("✓ All tests passed successfully!")
        print("✓ Card image URLs are properly configured")
    else:
        print("✗ Some tests failed - see details above")
    print("=" * 60)
    
    return len(cards_without_images) == 0 and len(cards_without_numbers) == 0 and len(invalid_urls) == 0

if __name__ == '__main__':
    success = test_card_images()
    exit(0 if success else 1)
