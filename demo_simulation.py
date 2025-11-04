#!/usr/bin/env python
"""
Demo script showing the combat simulation feature in action
This simulates what happens when a user clicks the Simulation button in the UI
"""

import requests
import json
from deck_builder import OnePieceDeckBuilder

def main():
    print("=" * 70)
    print("Combat Simulation Feature Demo")
    print("=" * 70)
    
    # Step 1: Build a player deck
    print("\n📦 Step 1: Building player's deck...")
    builder = OnePieceDeckBuilder()
    player_deck = builder.build_deck(strategy='aggressive', color='Red')
    print(f"   ✓ Built {player_deck['strategy']} {player_deck['color']} deck")
    print(f"   ✓ Leader: {player_deck['leader']['name']}")
    print(f"   ✓ Main deck: {len(player_deck['main_deck'])} cards")
    
    # Step 2: Get available opponent decks
    print("\n🎯 Step 2: Fetching available opponent decks...")
    response = requests.get('http://localhost:5000/api/opponent-decks')
    opponent_decks = response.json()['decks']
    print(f"   ✓ Found {len(opponent_decks)} tournament opponent decks:")
    for deck in opponent_decks:
        print(f"     - {deck['name']} ({deck['strategy']}, {deck['color']}) - WR: {deck['win_rate']}%")
    
    # Step 3: Run simulation against first opponent
    print("\n⚔️  Step 3: Running combat simulation...")
    opponent = opponent_decks[1]  # Blue Control Master
    print(f"   Selected opponent: {opponent['name']}")
    print(f"   Running 1000 simulations...")
    
    simulation_data = {
        'player_deck': player_deck,
        'opponent_deck_id': opponent['id'],
        'num_simulations': 1000
    }
    
    response = requests.post(
        'http://localhost:5000/api/simulate-combat',
        json=simulation_data
    )
    
    results = response.json()['results']
    
    # Step 4: Display results
    print("\n" + "=" * 70)
    print("📊 SIMULATION RESULTS")
    print("=" * 70)
    
    print(f"\n🏆 Matchup: {results['matchup_type']}")
    print(f"   Your Deck vs {results['opponent_name']}")
    print(f"   {results['opponent_description']}")
    
    print(f"\n📈 Win Rate: {results['win_rate']}%")
    print(f"   Wins: {results['wins']} / Losses: {results['losses']}")
    print(f"   (Based on {results['simulations_run']} simulations)")
    
    print(f"\n⏱️  Average Game Length:")
    print(f"   When you win: {results['avg_win_turns']:.1f} turns")
    print(f"   When you lose: {results['avg_loss_turns']:.1f} turns")
    
    print(f"\n📊 Deck Comparison:")
    print(f"   YOUR DECK:")
    deck1 = results['deck1_stats']
    print(f"     Strategy: {deck1['strategy']}")
    print(f"     Color: {deck1['color']}")
    print(f"     Avg Cost: {deck1['avg_cost']:.2f}")
    print(f"     Character Ratio: {deck1['character_ratio']:.1%}")
    
    print(f"\n   OPPONENT DECK:")
    deck2 = results['deck2_stats']
    print(f"     Strategy: {deck2['strategy']}")
    print(f"     Color: {deck2['color']}")
    print(f"     Avg Cost: {deck2['avg_cost']:.2f}")
    print(f"     Character Ratio: {deck2['character_ratio']:.1%}")
    
    print(f"\n💡 AI INSIGHTS:")
    for i, insight in enumerate(results['insights'], 1):
        print(f"   {i}. {insight}")
    
    if results['key_cards']:
        print(f"\n🎴 KEY CARDS IN YOUR DECK:")
        if results['key_cards']['high_power']:
            print(f"   High Power Threats: {', '.join(results['key_cards']['high_power'])}")
        if results['key_cards']['low_cost']:
            print(f"   Early Game Cards: {', '.join(results['key_cards']['low_cost'])}")
        if results['key_cards']['events']:
            print(f"   Key Events: {', '.join(results['key_cards']['events'])}")
    
    print("\n" + "=" * 70)
    print("✨ Combat simulation feature is fully operational!")
    print("=" * 70)
    
    # Interpret the result
    print("\n🎯 STRATEGIC RECOMMENDATION:")
    win_rate = results['win_rate']
    if win_rate >= 65:
        print("   ✅ EXCELLENT MATCHUP - You have a strong advantage!")
        print("   Play aggressively and leverage your strengths.")
    elif win_rate >= 55:
        print("   ✅ FAVORABLE MATCHUP - You're slightly favored.")
        print("   Play carefully and capitalize on opportunities.")
    elif win_rate >= 45:
        print("   ⚖️  EVEN MATCHUP - This could go either way.")
        print("   Focus on optimal play and avoid mistakes.")
    elif win_rate >= 35:
        print("   ⚠️  CHALLENGING MATCHUP - You're the underdog.")
        print("   Look for creative plays and exploit weaknesses.")
    else:
        print("   ⚠️  DIFFICULT MATCHUP - This will be tough.")
        print("   Consider sideboard options or deck adjustments.")
    
    print("\n")

if __name__ == '__main__':
    main()
