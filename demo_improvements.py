#!/usr/bin/env python
"""
Demo script showing the deck improvement suggestions feature
"""

from deck_builder import OnePieceDeckBuilder

def print_deck_summary(deck, title="Deck"):
    """Print a summary of a deck"""
    print(f"\n{title}")
    print("=" * 60)
    print(f"Leader: {deck['leader']['name']} ({', '.join(deck['leader']['colors'])})")
    print(f"Strategy: {deck.get('strategy', 'N/A')}")
    print(f"Cards: {len(deck['main_deck'])}")
    
    # Analyze type distribution
    type_counts = {}
    for card in deck['main_deck']:
        card_type = card['type']
        type_counts[card_type] = type_counts.get(card_type, 0) + 1
    
    print("\nType Distribution:")
    for card_type, count in sorted(type_counts.items()):
        ratio = count / len(deck['main_deck']) * 100
        print(f"  {card_type}: {count} ({ratio:.1f}%)")
    
    # Calculate average cost
    costs = [c.get('cost', 0) for c in deck['main_deck']]
    avg_cost = sum(costs) / len(costs) if costs else 0
    print(f"\nAverage Cost: {avg_cost:.2f}")
    
    if 'description' in deck:
        print(f"\n{deck['description']}")

def demo_improvements():
    """Demonstrate the deck improvement suggestions feature"""
    print("=" * 70)
    print("DECK IMPROVEMENT SUGGESTIONS - DEMO")
    print("=" * 70)
    print("\nThis demo shows how users can get improvement suggestions for their decks.")
    print("Three types of improvements are available:")
    print("  1. Balanced - Optimized for versatile gameplay")
    print("  2. Aggressive - Optimized for early pressure")
    print("  3. Tournament - Optimized for competitive play")
    
    # Initialize deck builder
    builder = OnePieceDeckBuilder()
    
    # Build an initial deck
    print("\n" + "=" * 70)
    print("STEP 1: Building Initial Deck")
    print("=" * 70)
    initial_deck = builder.build_deck(strategy='balanced', color='Red')
    print_deck_summary(initial_deck, "Initial Deck")
    
    # Simulate user collection
    print("\n" + "=" * 70)
    print("STEP 2: Simulating User Collection")
    print("=" * 70)
    owned_cards = {
        'Monkey D. Luffy': 4,
        'Portgas D. Ace': 4,
        'Roronoa Zoro': 4,
        'Sanji': 4,
        'Tony Tony Chopper': 4,
        'Nico Robin': 3,
        'Usopp': 3,
    }
    print("\nUser owns the following cards:")
    for card_name, qty in owned_cards.items():
        print(f"  {card_name}: {qty}x")
    
    # Get improvement suggestions
    print("\n" + "=" * 70)
    print("STEP 3: Generating Improvement Suggestions")
    print("=" * 70)
    print("\nAnalyzing deck and generating three optimized variations...")
    
    improvements = builder.suggest_improvements(initial_deck, owned_cards)
    
    # Show each improvement
    for improvement_type in ['balanced', 'aggressive', 'tournament']:
        improvement = improvements[improvement_type]
        
        print("\n" + "-" * 70)
        print(f"{improvement_type.upper()} IMPROVEMENT")
        print("-" * 70)
        print_deck_summary(improvement, f"{improvement_type.capitalize()} Deck")
        
        # Show changes
        changes = improvement['changes_from_current']
        print(f"\nChanges from original deck:")
        print(f"  Cards added: {len(changes['cards_added'])}")
        print(f"  Cards removed: {len(changes['cards_removed'])}")
        print(f"  Cards changed: {len(changes['cards_changed'])}")
        print(f"  Similarity: {changes['similarity_percentage']:.1f}%")
        
        # Show collection coverage
        coverage = improvement['collection_coverage']
        print(f"\nCollection coverage:")
        print(f"  Cards owned: {coverage['cards_owned']}/{coverage['total_cards']}")
        print(f"  Coverage: {coverage['coverage_percentage']:.1f}%")
        
        if coverage['cards_needed']:
            print(f"  Cards needed: {len(coverage['cards_needed'])}")
            # Show first 3 needed cards
            needed_list = list(coverage['cards_needed'].items())[:3]
            for card_name, qty in needed_list:
                print(f"    - {card_name}: {qty}x")
            if len(coverage['cards_needed']) > 3:
                print(f"    ... and {len(coverage['cards_needed']) - 3} more")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\n✓ Successfully generated three deck improvement suggestions")
    print("✓ Each suggestion optimizes for different play styles")
    print("✓ Collection coverage helps users see what cards they need")
    print("✓ Changes tracking helps users understand modifications")
    print("\nUsers can now:")
    print("  • Choose which improvement best fits their play style")
    print("  • See which cards they need to acquire")
    print("  • Save the improved deck to their collection")
    print("  • Continue iterating with more improvements")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    demo_improvements()
