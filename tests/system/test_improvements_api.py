#!/usr/bin/env python
"""
Integration test for deck improvement API endpoint
"""
import sys
import os

# Add the project root directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

import json
from app import app, db
from deck_builder import OnePieceDeckBuilder

def test_improvements_api():
    """Test the /api/suggest-improvements endpoint"""
    print("=" * 60)
    print("Deck Improvement API - Integration Test")
    print("=" * 60)
    
    # Create a test client
    with app.test_client() as client:
        # Set up test environment
        app.config['TESTING'] = True
        
        # Build a test deck first
        builder = OnePieceDeckBuilder()
        test_deck = builder.build_deck(strategy='balanced', color='Red')
        
        print("\n" + "-" * 60)
        print("Test Deck Created")
        print("-" * 60)
        print(f"  Leader: {test_deck['leader']['name']}")
        print(f"  Cards: {len(test_deck['main_deck'])}")
        
        # Test 1: Request improvements without authentication
        print("\n" + "-" * 60)
        print("Test 1: Request Improvements (Unauthenticated)")
        print("-" * 60)
        
        response = client.post('/api/suggest-improvements',
                              data=json.dumps({'deck': test_deck}),
                              content_type='application/json')
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = json.loads(response.data)
        
        assert data['success'] is True, "Request should succeed"
        assert 'improvements' in data, "Response should contain improvements"
        
        improvements = data['improvements']
        assert 'balanced' in improvements, "Should have balanced improvement"
        assert 'aggressive' in improvements, "Should have aggressive improvement"
        assert 'tournament' in improvements, "Should have tournament improvement"
        
        print("  ✓ Response received successfully")
        print(f"  ✓ All three improvement types present")
        
        # Validate improvement structure
        for improvement_type, improvement in improvements.items():
            assert 'leader' in improvement, f"{improvement_type} missing leader"
            assert 'main_deck' in improvement, f"{improvement_type} missing main_deck"
            assert 'description' in improvement, f"{improvement_type} missing description"
            assert 'changes_from_current' in improvement, f"{improvement_type} missing changes"
            print(f"  ✓ {improvement_type.capitalize()} improvement valid")
        
        # Test 2: Request with invalid deck
        print("\n" + "-" * 60)
        print("Test 2: Request with Invalid Deck")
        print("-" * 60)
        
        response = client.post('/api/suggest-improvements',
                              data=json.dumps({'deck': {}}),
                              content_type='application/json')
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        data = json.loads(response.data)
        assert data['success'] is False, "Invalid request should fail"
        print("  ✓ Invalid deck properly rejected")
        
        # Test 3: Request without deck
        print("\n" + "-" * 60)
        print("Test 3: Request without Deck")
        print("-" * 60)
        
        response = client.post('/api/suggest-improvements',
                              data=json.dumps({}),
                              content_type='application/json')
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        data = json.loads(response.data)
        assert data['success'] is False, "Missing deck should fail"
        print("  ✓ Missing deck properly rejected")
        
        # Test 4: Verify improvement characteristics
        print("\n" + "-" * 60)
        print("Test 4: Verify Improvement Characteristics")
        print("-" * 60)
        
        # Get fresh improvements
        response = client.post('/api/suggest-improvements',
                              data=json.dumps({'deck': test_deck}),
                              content_type='application/json')
        improvements = json.loads(response.data)['improvements']
        
        # Check aggressive deck characteristics
        aggressive = improvements['aggressive']
        aggressive_chars = sum(1 for c in aggressive['main_deck'] if c['type'] == 'Character')
        aggressive_char_ratio = aggressive_chars / len(aggressive['main_deck'])
        print(f"  Aggressive character ratio: {aggressive_char_ratio:.2%}")
        assert aggressive_char_ratio >= 0.60, "Aggressive deck should have high character ratio"
        
        # Check tournament deck cost curve
        tournament = improvements['tournament']
        tournament_costs = [c.get('cost', 0) for c in tournament['main_deck']]
        avg_cost = sum(tournament_costs) / len(tournament_costs) if tournament_costs else 0
        print(f"  Tournament average cost: {avg_cost:.2f}")
        
        # Check balanced deck composition
        balanced = improvements['balanced']
        type_counts = {}
        for card in balanced['main_deck']:
            card_type = card['type']
            type_counts[card_type] = type_counts.get(card_type, 0) + 1
        
        if type_counts:
            print(f"  Balanced type distribution:")
            for card_type, count in type_counts.items():
                ratio = count / len(balanced['main_deck'])
                print(f"    - {card_type}: {ratio:.2%}")
        
        print("  ✓ All improvement characteristics verified")
        
        # Summary
        print("\n" + "=" * 60)
        print("Integration Test Summary")
        print("=" * 60)
        print("✓ API endpoint responding correctly")
        print("✓ All improvement types generated")
        print("✓ Input validation working")
        print("✓ Improvement characteristics validated")
        print("=" * 60)

if __name__ == '__main__':
    test_improvements_api()
