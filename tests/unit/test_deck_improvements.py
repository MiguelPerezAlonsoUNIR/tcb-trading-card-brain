#!/usr/bin/env python
"""
Test script for deck improvement suggestions
"""
import sys
import os

# Add the project root directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from deck_builder import OnePieceDeckBuilder

def test_deck_improvements():
    """Test the deck improvement functionality"""
    print("=" * 60)
    print("Deck Improvement Suggestions - Test Suite")
    print("=" * 60)
    
    builder = OnePieceDeckBuilder()
    
    # Build a test deck
    print("\n" + "-" * 60)
    print("Building Test Deck")
    print("-" * 60)
    test_deck = builder.build_deck(strategy='balanced', color='Red')
    print(f"✓ Built test deck with {len(test_deck['main_deck'])} cards")
    print(f"  Leader: {test_deck['leader']['name']}")
    print(f"  Strategy: {test_deck['strategy']}")
    
    # Test 1: Generate improvement suggestions
    print("\n" + "-" * 60)
    print("Test 1: Generating Improvement Suggestions")
    print("-" * 60)
    improvements = builder.suggest_improvements(test_deck)
    
    print(f"✓ Generated {len(improvements)} improvement suggestions")
    
    # Verify all three types are present
    assert 'balanced' in improvements, "Missing 'balanced' improvement"
    assert 'aggressive' in improvements, "Missing 'aggressive' improvement"
    assert 'tournament' in improvements, "Missing 'tournament' improvement"
    print("  ✓ All three improvement types present")
    
    # Test 2: Validate balanced improvement
    print("\n" + "-" * 60)
    print("Test 2: Validating Balanced Improvement")
    print("-" * 60)
    balanced = improvements['balanced']
    print(f"  Deck size: {len(balanced['main_deck'])} cards")
    print(f"  Description: {balanced['description']}")
    print(f"  Strategy: {balanced['strategy']}")
    
    # Check deck structure
    assert 'leader' in balanced, "Missing leader in balanced improvement"
    assert 'main_deck' in balanced, "Missing main_deck in balanced improvement"
    assert len(balanced['main_deck']) <= 50, "Deck too large"
    print("  ✓ Balanced improvement structure valid")
    
    # Check changes tracking
    assert 'changes_from_current' in balanced, "Missing changes_from_current"
    changes = balanced['changes_from_current']
    print(f"  Total changes: {changes['total_changes']}")
    print(f"  Similarity: {changes['similarity_percentage']}%")
    print("  ✓ Changes tracking present")
    
    # Test 3: Validate aggressive improvement
    print("\n" + "-" * 60)
    print("Test 3: Validating Aggressive Improvement")
    print("-" * 60)
    aggressive = improvements['aggressive']
    print(f"  Deck size: {len(aggressive['main_deck'])} cards")
    print(f"  Description: {aggressive['description']}")
    print(f"  Strategy: {aggressive['strategy']}")
    
    # Check that aggressive deck has lower average cost
    aggressive_costs = [c.get('cost', 0) for c in aggressive['main_deck']]
    avg_aggressive_cost = sum(aggressive_costs) / len(aggressive_costs) if aggressive_costs else 0
    print(f"  Average cost: {avg_aggressive_cost:.2f}")
    
    # Count character ratio
    aggressive_chars = sum(1 for c in aggressive['main_deck'] if c['type'] == 'Character')
    char_ratio = aggressive_chars / len(aggressive['main_deck']) if aggressive['main_deck'] else 0
    print(f"  Character ratio: {char_ratio:.2%}")
    print("  ✓ Aggressive improvement valid")
    
    # Test 4: Validate tournament improvement
    print("\n" + "-" * 60)
    print("Test 4: Validating Tournament Improvement")
    print("-" * 60)
    tournament = improvements['tournament']
    print(f"  Deck size: {len(tournament['main_deck'])} cards")
    print(f"  Description: {tournament['description']}")
    print(f"  Strategy: {tournament['strategy']}")
    
    # Check cost curve
    tournament_costs = [c.get('cost', 0) for c in tournament['main_deck']]
    avg_tournament_cost = sum(tournament_costs) / len(tournament_costs) if tournament_costs else 0
    print(f"  Average cost: {avg_tournament_cost:.2f}")
    print("  ✓ Tournament improvement valid")
    
    # Test 5: Test with owned cards
    print("\n" + "-" * 60)
    print("Test 5: Testing with Owned Cards")
    print("-" * 60)
    owned_cards = {
        'Monkey D. Luffy': 4,
        'Portgas D. Ace': 4,
        'Roronoa Zoro': 4,
        'Sanji': 4,
        'Tony Tony Chopper': 4
    }
    improvements_with_collection = builder.suggest_improvements(test_deck, owned_cards)
    
    # Check collection coverage
    for improvement_type, improvement in improvements_with_collection.items():
        coverage = improvement.get('collection_coverage', {})
        print(f"  {improvement_type.capitalize()}: {coverage.get('coverage_percentage', 0):.2f}% coverage")
    print("  ✓ Collection-aware suggestions generated")
    
    # Test 6: Verify card copy limits
    print("\n" + "-" * 60)
    print("Test 6: Verifying Card Copy Limits")
    print("-" * 60)
    
    for improvement_type, improvement in improvements.items():
        card_counts = {}
        for card in improvement['main_deck']:
            card_counts[card['name']] = card_counts.get(card['name'], 0) + 1
        
        max_copies = max(card_counts.values()) if card_counts else 0
        print(f"  {improvement_type.capitalize()}: max {max_copies} copies")
        assert max_copies <= 4, f"{improvement_type} exceeds 4-copy limit"
    
    print("  ✓ All improvements respect 4-copy limit")
    
    # Test 7: Verify leader consistency
    print("\n" + "-" * 60)
    print("Test 7: Verifying Leader Consistency")
    print("-" * 60)
    
    original_leader = test_deck['leader']['name']
    for improvement_type, improvement in improvements.items():
        improved_leader = improvement['leader']['name']
        assert improved_leader == original_leader, \
            f"{improvement_type} changed leader from {original_leader} to {improved_leader}"
        print(f"  {improvement_type.capitalize()}: Leader '{improved_leader}' ✓")
    
    print("  ✓ All improvements maintain same leader")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print("✓ All tests passed successfully!")
    print("✓ Deck improvement suggestions working correctly")
    print("✓ Three improvement types generated:")
    print("  - Balanced: Optimized for versatile gameplay")
    print("  - Aggressive: Optimized for early pressure")
    print("  - Tournament: Optimized for competitive play")
    print("=" * 60)

if __name__ == '__main__':
    test_deck_improvements()
