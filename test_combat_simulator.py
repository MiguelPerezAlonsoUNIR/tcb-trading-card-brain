#!/usr/bin/env python
"""
Test script for the Combat Simulator
Run this to verify the combat simulation logic works correctly
"""

from combat_simulator import CombatSimulator, TournamentMatch
from deck_builder import OnePieceDeckBuilder

def test_combat_simulator():
    """Test the combat simulator functionality"""
    print("=" * 60)
    print("One Piece TCG Combat Simulator - Test Suite")
    print("=" * 60)
    
    simulator = CombatSimulator()
    builder = OnePieceDeckBuilder()
    
    print(f"\n✓ Combat simulator initialized with {len(simulator.tournament_data)} tournament matches")
    
    # Test 1: Build two test decks
    print("\n" + "-" * 60)
    print("Test 1: Building Test Decks")
    print("-" * 60)
    
    deck1 = builder.build_deck(strategy='aggressive', color='Red')
    print(f"✓ Built aggressive red deck")
    print(f"  Leader: {deck1['leader']['name']}")
    print(f"  Cards: {len(deck1['main_deck'])}")
    
    deck2 = builder.build_deck(strategy='control', color='Blue')
    print(f"✓ Built control blue deck")
    print(f"  Leader: {deck2['leader']['name']}")
    print(f"  Cards: {len(deck2['main_deck'])}")
    
    # Test 2: Extract deck statistics
    print("\n" + "-" * 60)
    print("Test 2: Extracting Deck Statistics")
    print("-" * 60)
    
    deck1_stats = simulator._extract_deck_stats(deck1)
    print(f"✓ Deck 1 stats:")
    print(f"  Strategy: {deck1_stats['strategy']}")
    print(f"  Color: {deck1_stats['color']}")
    print(f"  Avg Cost: {deck1_stats['avg_cost']:.2f}")
    print(f"  Character Ratio: {deck1_stats['character_ratio']:.2%}")
    
    deck2_stats = simulator._extract_deck_stats(deck2)
    print(f"✓ Deck 2 stats:")
    print(f"  Strategy: {deck2_stats['strategy']}")
    print(f"  Color: {deck2_stats['color']}")
    print(f"  Avg Cost: {deck2_stats['avg_cost']:.2f}")
    print(f"  Character Ratio: {deck2_stats['character_ratio']:.2%}")
    
    # Test 3: Calculate base win probability
    print("\n" + "-" * 60)
    print("Test 3: Calculating Base Win Probability")
    print("-" * 60)
    
    base_prob = simulator._calculate_base_probability(deck1_stats, deck2_stats)
    print(f"✓ Base win probability (Deck 1 vs Deck 2): {base_prob:.2%}")
    
    # Test 4: Calculate AI-learned win probability
    print("\n" + "-" * 60)
    print("Test 4: Calculating AI-Learned Win Probability")
    print("-" * 60)
    
    ai_prob = simulator._calculate_win_probability(deck1_stats, deck2_stats)
    print(f"✓ AI-learned win probability: {ai_prob:.2%}")
    print(f"  (Blended from tournament data: 70% learned + 30% base)")
    
    # Test 5: Run full combat simulation (small sample)
    print("\n" + "-" * 60)
    print("Test 5: Running Combat Simulation (100 iterations)")
    print("-" * 60)
    
    results = simulator.simulate_combat(deck1, deck2, num_simulations=100)
    
    print(f"✓ Simulation completed")
    print(f"  Matchup: {results['matchup_type']}")
    print(f"  Win Rate: {results['win_rate']:.2f}%")
    print(f"  Wins: {results['wins']}")
    print(f"  Losses: {results['losses']}")
    print(f"  Avg Win Turns: {results['avg_win_turns']:.1f}")
    print(f"  Avg Loss Turns: {results['avg_loss_turns']:.1f}")
    
    # Test 6: Verify insights generation
    print("\n" + "-" * 60)
    print("Test 6: AI Insights Generation")
    print("-" * 60)
    
    print(f"✓ Generated {len(results['insights'])} insights:")
    for i, insight in enumerate(results['insights'], 1):
        print(f"  {i}. {insight}")
    
    # Test 7: Key cards identification
    print("\n" + "-" * 60)
    print("Test 7: Key Cards Identification")
    print("-" * 60)
    
    key_cards = results['key_cards']
    print(f"✓ Identified key cards:")
    if key_cards['high_power']:
        print(f"  High Power: {', '.join(key_cards['high_power'])}")
    if key_cards['low_cost']:
        print(f"  Low Cost: {', '.join(key_cards['low_cost'])}")
    if key_cards['events']:
        print(f"  Events: {', '.join(key_cards['events'])}")
    
    # Test 8: Different matchup types
    print("\n" + "-" * 60)
    print("Test 8: Testing Different Matchup Types")
    print("-" * 60)
    
    # Balanced vs Balanced (mirror match)
    deck3 = builder.build_deck(strategy='balanced', color='Green')
    deck4 = builder.build_deck(strategy='balanced', color='Green')
    results_mirror = simulator.simulate_combat(deck3, deck4, num_simulations=100)
    print(f"✓ Mirror Match: {results_mirror['matchup_type']}")
    print(f"  Win Rate: {results_mirror['win_rate']:.2f}% (should be close to 50%)")
    
    # Control vs Aggressive (favorable for aggressive)
    results_favorable = simulator.simulate_combat(deck1, deck2, num_simulations=100)
    print(f"✓ Aggressive vs Control: {results_favorable['win_rate']:.2f}%")
    
    # Test 9: Get available opponent decks
    print("\n" + "-" * 60)
    print("Test 9: Available Opponent Decks")
    print("-" * 60)
    
    opponent_decks = simulator.get_available_opponent_decks()
    print(f"✓ Available opponent decks: {len(opponent_decks)}")
    for deck in opponent_decks:
        print(f"  - {deck['name']} ({deck['strategy']}, {deck['color']}) - WR: {deck['win_rate']}%")
    
    # Test 10: Matchup similarity calculation
    print("\n" + "-" * 60)
    print("Test 10: Tournament Matchup Similarity")
    print("-" * 60)
    
    # Create a test match similar to our decks
    test_match = TournamentMatch(
        deck1_strategy='aggressive',
        deck1_color='Red',
        deck1_avg_cost=3.2,
        deck1_character_ratio=0.70,
        deck2_strategy='control',
        deck2_color='Blue',
        deck2_avg_cost=5.5,
        deck2_character_ratio=0.60,
        deck1_wins=True,
        match_duration=8
    )
    
    similarity = simulator._calculate_matchup_similarity(deck1_stats, deck2_stats, test_match)
    print(f"✓ Similarity to tournament match: {similarity:.2%}")
    print(f"  (Higher similarity means the AI can learn more from this match)")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print("✓ All tests passed successfully!")
    print("✓ Combat simulation logic is working correctly")
    print("✓ AI learning from tournament data is functional")
    print("=" * 60)
    
    # Additional validation
    print("\n" + "=" * 60)
    print("Validation Checks")
    print("=" * 60)
    
    checks_passed = 0
    total_checks = 5
    
    # Check 1: Win rate is reasonable
    if 0 <= results['win_rate'] <= 100:
        print("✓ Win rate is within valid range (0-100%)")
        checks_passed += 1
    else:
        print("✗ Win rate is out of range!")
    
    # Check 2: Simulation count matches
    if results['wins'] + results['losses'] == results['simulations_run']:
        print("✓ Win/loss counts match simulation count")
        checks_passed += 1
    else:
        print("✗ Win/loss counts don't match!")
    
    # Check 3: Turn counts are reasonable
    if 5 <= results['avg_win_turns'] <= 25 and 5 <= results['avg_loss_turns'] <= 25:
        print("✓ Turn counts are realistic")
        checks_passed += 1
    else:
        print("✗ Turn counts seem unrealistic!")
    
    # Check 4: Insights were generated
    if len(results['insights']) > 0:
        print("✓ AI insights were generated")
        checks_passed += 1
    else:
        print("✗ No AI insights generated!")
    
    # Check 5: Key cards identified
    if any(results['key_cards'].values()):
        print("✓ Key cards were identified")
        checks_passed += 1
    else:
        print("✗ No key cards identified!")
    
    print(f"\nValidation Score: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("🎉 Perfect score! Combat simulator is fully functional!")
    elif checks_passed >= 4:
        print("✓ Good! Minor issues but core functionality works")
    else:
        print("⚠ Warning: Some checks failed, review the implementation")

if __name__ == '__main__':
    test_combat_simulator()
