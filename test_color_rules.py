#!/usr/bin/env python
"""
Test script to verify One Piece TCG color rules are enforced
According to the official rules, cards in a deck must match the leader's color(s)
"""

from deck_builder import OnePieceDeckBuilder
from cards_data import ONEPIECE_CARDS


def test_single_color_leader_rule():
    """Test that single-color leaders only get cards matching their color"""
    print("=" * 60)
    print("Test: Single Color Leader Rule Enforcement")
    print("=" * 60)
    
    builder = OnePieceDeckBuilder()
    
    # Test with Red leader (Monkey D. Luffy)
    print("\n1. Testing Red leader (Monkey D. Luffy)...")
    deck = builder.build_deck(strategy='balanced', color='Red', leader='Monkey D. Luffy')
    leader = deck['leader']
    print(f"   Leader: {leader['name']} - Colors: {leader['colors']}")
    
    # Check that all cards in deck share at least one color with leader
    invalid_cards = []
    for card in deck['main_deck']:
        if not any(lc in card['colors'] for lc in leader['colors']):
            invalid_cards.append(card)
    
    if invalid_cards:
        print(f"   ✗ FAILED: Found {len(invalid_cards)} cards that don't match leader colors:")
        for card in invalid_cards[:5]:  # Show first 5
            print(f"     - {card['name']} ({card['colors']})")
        return False
    else:
        print(f"   ✓ PASSED: All {len(deck['main_deck'])} cards match leader color")
    
    # Test with Blue leader (Nami)
    print("\n2. Testing Blue leader (Nami)...")
    deck = builder.build_deck(strategy='aggressive', color='Blue', leader='Nami')
    leader = deck['leader']
    print(f"   Leader: {leader['name']} - Colors: {leader['colors']}")
    
    invalid_cards = []
    for card in deck['main_deck']:
        if not any(lc in card['colors'] for lc in leader['colors']):
            invalid_cards.append(card)
    
    if invalid_cards:
        print(f"   ✗ FAILED: Found {len(invalid_cards)} cards that don't match leader colors:")
        for card in invalid_cards[:5]:
            print(f"     - {card['name']} ({card['colors']})")
        return False
    else:
        print(f"   ✓ PASSED: All {len(deck['main_deck'])} cards match leader color")
    
    return True


def test_multi_color_leader_rule():
    """Test that multi-color leaders allow cards from any of their colors"""
    print("\n" + "=" * 60)
    print("Test: Multi-Color Leader Rule Enforcement")
    print("=" * 60)
    
    builder = OnePieceDeckBuilder()
    
    # Test with Blue/Black leader (Trafalgar Law)
    print("\n1. Testing Blue/Black leader (Trafalgar Law)...")
    deck = builder.build_deck(strategy='balanced', color='any', leader='Trafalgar Law')
    leader = deck['leader']
    print(f"   Leader: {leader['name']} - Colors: {leader['colors']}")
    
    # Check that all cards share at least one color with leader
    invalid_cards = []
    blue_cards = 0
    black_cards = 0
    multi_color_cards = 0
    
    for card in deck['main_deck']:
        # Card must have at least one color matching the leader
        if not any(lc in card['colors'] for lc in leader['colors']):
            invalid_cards.append(card)
        else:
            # Count distribution
            if 'Blue' in card['colors'] and 'Black' in card['colors']:
                multi_color_cards += 1
            elif 'Blue' in card['colors']:
                blue_cards += 1
            elif 'Black' in card['colors']:
                black_cards += 1
    
    if invalid_cards:
        print(f"   ✗ FAILED: Found {len(invalid_cards)} cards that don't match leader colors:")
        for card in invalid_cards[:5]:
            print(f"     - {card['name']} ({card['colors']})")
        return False
    else:
        print(f"   ✓ PASSED: All {len(deck['main_deck'])} cards match at least one leader color")
        print(f"   Distribution: {blue_cards} Blue, {black_cards} Black, {multi_color_cards} Blue/Black")
    
    return True


def test_any_color_parameter():
    """Test that 'any' color parameter still respects leader colors"""
    print("\n" + "=" * 60)
    print("Test: 'Any' Color Parameter Still Enforces Leader Colors")
    print("=" * 60)
    
    builder = OnePieceDeckBuilder()
    
    # Build deck with 'any' color but specific leader
    print("\n1. Testing 'any' color with Green leader (Roronoa Zoro)...")
    deck = builder.build_deck(strategy='control', color='any', leader='Roronoa Zoro')
    leader = deck['leader']
    print(f"   Leader: {leader['name']} - Colors: {leader['colors']}")
    
    # All cards should still only be Green (or include Green in multi-color)
    invalid_cards = []
    for card in deck['main_deck']:
        if not any(lc in card['colors'] for lc in leader['colors']):
            invalid_cards.append(card)
    
    if invalid_cards:
        print(f"   ✗ FAILED: Found {len(invalid_cards)} cards that don't match leader colors:")
        for card in invalid_cards[:5]:
            print(f"     - {card['name']} ({card['colors']})")
        return False
    else:
        print(f"   ✓ PASSED: All {len(deck['main_deck'])} cards match leader color")
        print(f"   'any' parameter correctly enforces leader color matching")
    
    return True


def test_color_distribution():
    """Test and display color distribution in built decks"""
    print("\n" + "=" * 60)
    print("Test: Color Distribution Analysis")
    print("=" * 60)
    
    builder = OnePieceDeckBuilder()
    
    # Test each color
    colors_to_test = ['Red', 'Blue', 'Green', 'Purple']
    
    for color in colors_to_test:
        print(f"\n{color} Deck:")
        deck = builder.build_deck(strategy='balanced', color=color)
        leader = deck['leader']
        
        # Count colors
        color_counts = {}
        for card in deck['main_deck']:
            for c in card['colors']:
                color_counts[c] = color_counts.get(c, 0) + 1
        
        print(f"   Leader: {leader['name']} ({', '.join(leader['colors'])})")
        print(f"   Color distribution in deck: {color_counts}")
        
        # Verify all cards match leader
        matches_leader = all(
            any(lc in card['colors'] for lc in leader['colors'])
            for card in deck['main_deck']
        )
        
        if matches_leader:
            print(f"   ✓ All cards match leader color(s)")
        else:
            print(f"   ✗ Some cards don't match leader color(s)")
            return False
    
    return True


def main():
    """Run all color rule tests"""
    print("\n" + "=" * 60)
    print("One Piece TCG Color Rules - Test Suite")
    print("=" * 60)
    print("\nTesting enforcement of the rule:")
    print("'Cards in a deck can only be from the same color(s) as the leader'")
    
    results = []
    
    # Run all tests
    results.append(("Single Color Leader", test_single_color_leader_rule()))
    results.append(("Multi-Color Leader", test_multi_color_leader_rule()))
    results.append(("'Any' Color Parameter", test_any_color_parameter()))
    results.append(("Color Distribution", test_color_distribution()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 60)
    if passed == total:
        print(f"✓ All {total} tests passed!")
        print("✓ One Piece TCG color rules are correctly enforced")
    else:
        print(f"✗ {total - passed} of {total} tests failed")
        print("✗ Color rules need to be fixed")
    print("=" * 60)
    
    return passed == total


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
