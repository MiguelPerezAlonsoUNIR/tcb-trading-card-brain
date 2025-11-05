#!/usr/bin/env python
"""
Test to verify all structure decks have exactly 50 cards
"""

import sys
from structure_decks import STRUCTURE_DECKS

def test_all_structure_decks_have_50_cards():
    """Verify that all structure decks have exactly 50 cards (excluding leader)"""
    print("\n" + "="*70)
    print("Testing Structure Deck Card Counts")
    print("="*70)
    
    failed_decks = []
    
    for code in sorted(STRUCTURE_DECKS.keys()):
        deck = STRUCTURE_DECKS[code]
        total = sum(deck['cards'].values())
        
        if total != 50:
            failed_decks.append((code, deck['name'], total))
            print(f"✗ {code}: {deck['name']} - {total} cards (expected 50)")
        else:
            print(f"✓ {code}: {deck['name']} - {total} cards")
    
    print("="*70)
    
    if failed_decks:
        print(f"\n✗ {len(failed_decks)} deck(s) do not have 50 cards:")
        for code, name, total in failed_decks:
            print(f"  - {code} ({name}): {total} cards")
        return False
    else:
        print(f"\n✓ All {len(STRUCTURE_DECKS)} structure decks have exactly 50 cards!")
        return True

def main():
    """Run the test"""
    try:
        success = test_all_structure_decks_have_50_cards()
        return 0 if success else 1
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
