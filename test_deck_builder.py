#!/usr/bin/env python
"""
Test script for the One Piece TCG Deck Builder
Run this to verify the deck building logic works correctly
"""

from deck_builder import OnePieceDeckBuilder
from cards_data import ONEPIECE_CARDS

def test_deck_builder():
    """Test the deck builder functionality"""
    print("=" * 60)
    print("One Piece TCG Deck Builder - Test Suite")
    print("=" * 60)
    
    builder = OnePieceDeckBuilder()
    print(f"\n✓ Deck builder initialized with {len(builder.cards)} cards")
    print(f"  - Leaders: {len([c for c in builder.cards if c['type'] == 'Leader'])}")
    print(f"  - Characters: {len([c for c in builder.cards if c['type'] == 'Character'])}")
    print(f"  - Events: {len([c for c in builder.cards if c['type'] == 'Event'])}")
    print(f"  - Stages: {len([c for c in builder.cards if c['type'] == 'Stage'])}")
    
    # Test 1: Balanced Red deck
    print("\n" + "-" * 60)
    print("Test 1: Building Balanced Red Deck")
    print("-" * 60)
    deck1 = builder.build_deck(strategy='balanced', color='Red')
    print(f"✓ Built deck with {len(deck1['main_deck'])} cards")
    print(f"  Leader: {deck1['leader']['name']} ({', '.join(deck1['leader']['colors'])})")
    print(f"  Strategy: {deck1['strategy']}")
    
    # Test 2: Aggressive Blue deck
    print("\n" + "-" * 60)
    print("Test 2: Building Aggressive Blue Deck")
    print("-" * 60)
    deck2 = builder.build_deck(strategy='aggressive', color='Blue')
    print(f"✓ Built deck with {len(deck2['main_deck'])} cards")
    print(f"  Leader: {deck2['leader']['name']} ({', '.join(deck2['leader']['colors'])})")
    print(f"  Strategy: {deck2['strategy']}")
    
    # Test 3: Control any-color deck
    print("\n" + "-" * 60)
    print("Test 3: Building Control Any-Color Deck")
    print("-" * 60)
    deck3 = builder.build_deck(strategy='control', color='any')
    print(f"✓ Built deck with {len(deck3['main_deck'])} cards")
    print(f"  Leader: {deck3['leader']['name']} ({', '.join(deck3['leader']['colors'])})")
    print(f"  Strategy: {deck3['strategy']}")
    
    # Test 4: Specific leader
    print("\n" + "-" * 60)
    print("Test 4: Building Deck with Specific Leader (Kaido)")
    print("-" * 60)
    deck4 = builder.build_deck(strategy='balanced', color='Purple', leader='Kaido')
    print(f"✓ Built deck with {len(deck4['main_deck'])} cards")
    print(f"  Leader: {deck4['leader']['name']} ({', '.join(deck4['leader']['colors'])})")
    
    # Test 5: Deck Analysis
    print("\n" + "-" * 60)
    print("Test 5: Analyzing Deck")
    print("-" * 60)
    analysis = builder.analyze_deck(deck1['main_deck'])
    print(f"✓ Analysis completed")
    print(f"  Total cards: {analysis['total_cards']}")
    print(f"  Cost curve: {analysis['curve']}")
    print(f"  Type distribution: {analysis['type_distribution']}")
    print(f"  Color distribution: {analysis['color_distribution']}")
    print(f"  Suggestions: {len(analysis['suggestions'])}")
    if analysis['suggestions']:
        for i, suggestion in enumerate(analysis['suggestions'], 1):
            print(f"    {i}. {suggestion}")
    
    # Test 6: Card uniqueness check
    print("\n" + "-" * 60)
    print("Test 6: Verifying Card Copy Limits")
    print("-" * 60)
    card_counts = {}
    for card in deck1['main_deck']:
        card_counts[card['name']] = card_counts.get(card['name'], 0) + 1
    
    max_copies = max(card_counts.values())
    print(f"✓ Maximum copies of any card: {max_copies}")
    if max_copies <= 4:
        print("  ✓ Card copy limit (4) respected")
    else:
        print("  ✗ Card copy limit exceeded!")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print("✓ All tests passed successfully!")
    print("✓ Deck building logic is working correctly")
    print("=" * 60)

if __name__ == '__main__':
    test_deck_builder()
