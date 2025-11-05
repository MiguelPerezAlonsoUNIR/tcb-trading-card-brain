#!/usr/bin/env python
"""
Test to verify that deck builder creates 50-card decks (without counting the leader)
"""

from deck_builder import OnePieceDeckBuilder
from cards_data import ONEPIECE_CARDS

def test_50_card_deck_creation():
    """Test that all deck building strategies create 50-card decks when possible"""
    print("=" * 60)
    print("Testing 50-Card Deck Creation")
    print("=" * 60)
    
    builder = OnePieceDeckBuilder()
    
    # Get all leaders and check their card pool sizes
    leaders = [c for c in ONEPIECE_CARDS if c['type'] == 'Leader']
    
    print(f"\nTotal Leaders: {len(leaders)}")
    print("\nLeader Card Pool Analysis:")
    for leader in leaders:
        available_cards = [
            c for c in ONEPIECE_CARDS
            if c['type'] != 'Leader' and
            any(lc in c['colors'] for lc in leader['colors'])
        ]
        max_possible = len(available_cards) * 4
        can_build_50 = "✓" if max_possible >= 50 else "✗"
        print(f"  {can_build_50} {leader['name']:20} ({', '.join(leader['colors']):15}): "
              f"{len(available_cards)} unique cards ({max_possible} max)")
    
    print("\n" + "-" * 60)
    print("Testing Deck Creation with Different Strategies")
    print("-" * 60)
    
    test_cases = [
        ('balanced', 'Red', None),
        ('balanced', 'Blue', None),
        ('balanced', 'Green', None),
        ('balanced', 'Purple', None),
        ('balanced', 'any', None),
        ('aggressive', 'Red', None),
        ('aggressive', 'Blue', None),
        ('aggressive', 'Green', None),
        ('aggressive', 'Purple', None),
        ('aggressive', 'any', None),
        ('control', 'Red', None),
        ('control', 'Blue', None),
        ('control', 'Green', None),
        ('control', 'Purple', None),
        ('control', 'any', None),
        ('balanced', 'Purple', 'Kaido'),  # Test with specific leader
        ('balanced', 'Red', 'Monkey D. Luffy'),  # Test with specific leader
    ]
    
    failed_tests = []
    passed_tests = []
    
    for strategy, color, leader in test_cases:
        deck = builder.build_deck(strategy=strategy, color=color, leader=leader)
        main_deck_size = len(deck['main_deck'])
        leader_name = deck['leader']['name']
        leader_colors = ', '.join(deck['leader']['colors'])
        
        test_name = f"{strategy.capitalize()} {color} deck"
        if leader:
            test_name += f" (Leader: {leader})"
        
        if main_deck_size == 50:
            status = "✓ PASS"
            passed_tests.append(test_name)
        else:
            status = "✗ FAIL"
            failed_tests.append((test_name, main_deck_size))
        
        print(f"{status}: {test_name}")
        print(f"    Leader: {leader_name} ({leader_colors})")
        print(f"    Main Deck: {main_deck_size} cards")
        
        # Verify card copy limits
        card_counts = {}
        for card in deck['main_deck']:
            card_counts[card['name']] = card_counts.get(card['name'], 0) + 1
        
        max_copies = max(card_counts.values()) if card_counts else 0
        if max_copies > 4:
            print(f"    ⚠ WARNING: Card copy limit exceeded! Max: {max_copies}")
            failed_tests.append((test_name, f"Copy limit exceeded: {max_copies}"))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Total Tests: {len(test_cases)}")
    print(f"Passed: {len(passed_tests)}")
    print(f"Failed: {len(failed_tests)}")
    
    if failed_tests:
        print("\nFailed Tests:")
        for test_name, detail in failed_tests:
            if isinstance(detail, int):
                print(f"  - {test_name}: {detail} cards (expected 50)")
            else:
                print(f"  - {test_name}: {detail}")
        print("\nNote: Some failures may be expected if the card database doesn't have")
        print("enough cards for certain color combinations (e.g., Black, Yellow).")
    else:
        print("\n✓ All tests passed! All viable color combinations create 50-card decks.")
    
    print("=" * 60)
    
    return len(failed_tests) == 0

if __name__ == '__main__':
    success = test_50_card_deck_creation()
    exit(0 if success else 1)
