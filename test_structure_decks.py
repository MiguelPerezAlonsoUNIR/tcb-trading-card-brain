#!/usr/bin/env python
"""
Test script for structure deck functionality
"""

import sys
import json
from app import app, db
from models import User, UserCollection
from auth import hash_password

def setup_test_db():
    """Setup test database with a test user"""
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create a test user
        test_user = User(
            username='testuser',
            password_hash=hash_password('password123')
        )
        db.session.add(test_user)
        db.session.commit()
        return test_user.id

def test_get_structure_decks():
    """Test getting list of structure decks"""
    print("\n" + "="*60)
    print("Test 1: Get Structure Decks List")
    print("="*60)
    
    with app.test_client() as client:
        response = client.get('/api/structure-decks')
        data = json.loads(response.data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert data['success'] == True, "Response should be successful"
        assert 'decks' in data, "Response should contain 'decks'"
        assert len(data['decks']) == 28, f"Expected 28 decks, got {len(data['decks'])}"
        
        print(f"✓ Successfully retrieved {len(data['decks'])} structure decks")
        print(f"  First deck: {data['decks'][0]['code']} - {data['decks'][0]['name']}")
        print(f"  Last deck: {data['decks'][-1]['code']} - {data['decks'][-1]['name']}")

def test_get_structure_deck_details():
    """Test getting details of a specific structure deck"""
    print("\n" + "="*60)
    print("Test 2: Get Structure Deck Details")
    print("="*60)
    
    with app.test_client() as client:
        # Test ST-01
        response = client.get('/api/structure-decks/ST-01')
        data = json.loads(response.data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert data['success'] == True, "Response should be successful"
        assert 'deck' in data, "Response should contain 'deck'"
        assert data['deck']['code'] == 'ST-01', "Deck code should be ST-01"
        assert 'cards' in data['deck'], "Deck should contain cards"
        
        total_cards = sum(data['deck']['cards'].values())
        print(f"✓ Retrieved ST-01 details")
        print(f"  Name: {data['deck']['name']}")
        print(f"  Color: {data['deck']['color']}")
        print(f"  Leader: {data['deck']['leader']}")
        print(f"  Total cards: {total_cards}")
        print(f"  Unique cards: {len(data['deck']['cards'])}")
        
        # Test invalid deck
        response = client.get('/api/structure-decks/ST-99')
        data = json.loads(response.data)
        assert response.status_code == 404, f"Expected 404 for invalid deck, got {response.status_code}"
        print(f"✓ Correctly returned 404 for invalid deck code")

def test_add_structure_deck_to_collection():
    """Test adding a structure deck to user's collection"""
    print("\n" + "="*60)
    print("Test 3: Add Structure Deck to Collection")
    print("="*60)
    
    user_id = setup_test_db()
    
    with app.test_client() as client:
        # Login first
        response = client.post('/api/login', 
            json={'username': 'testuser', 'password': 'password123'},
            content_type='application/json'
        )
        assert response.status_code == 200, "Login should succeed"
        
        # Add ST-01 to collection
        response = client.post('/api/collection/add-structure-deck',
            json={'deck_code': 'ST-01'},
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert data['success'] == True, "Response should be successful"
        assert data['deck_code'] == 'ST-01', "Deck code should be ST-01"
        assert 'added_cards' in data, "Response should contain added_cards"
        
        print(f"✓ Successfully added ST-01 to collection")
        print(f"  Total cards added: {data['total_cards_modified']}")
        print(f"  New cards: {len(data['added_cards'])}")
        print(f"  Updated cards: {len(data['updated_cards'])}")
        
        # Verify cards were added to database
        with app.app_context():
            collection = UserCollection.query.filter_by(user_id=user_id).all()
            print(f"✓ Verified {len(collection)} cards in database")
            
            # Check a specific card
            luffy = UserCollection.query.filter_by(
                user_id=user_id, 
                card_name='Monkey D. Luffy'
            ).first()
            assert luffy is not None, "Luffy should be in collection"
            assert luffy.quantity == 1, f"Luffy quantity should be 1, got {luffy.quantity}"
            print(f"✓ Verified Luffy in collection with quantity {luffy.quantity}")

def test_add_structure_deck_twice():
    """Test adding the same structure deck twice (should update quantities)"""
    print("\n" + "="*60)
    print("Test 4: Add Structure Deck Twice (Update Quantities)")
    print("="*60)
    
    user_id = setup_test_db()
    
    with app.test_client() as client:
        # Login
        client.post('/api/login', 
            json={'username': 'testuser', 'password': 'password123'},
            content_type='application/json'
        )
        
        # Add ST-02 first time
        response1 = client.post('/api/collection/add-structure-deck',
            json={'deck_code': 'ST-02'},
            content_type='application/json'
        )
        data1 = json.loads(response1.data)
        
        print(f"✓ First addition: {data1['total_cards_modified']} cards modified")
        print(f"  New cards: {len(data1['added_cards'])}")
        print(f"  Updated cards: {len(data1['updated_cards'])}")
        
        # Add ST-02 second time
        response2 = client.post('/api/collection/add-structure-deck',
            json={'deck_code': 'ST-02'},
            content_type='application/json'
        )
        data2 = json.loads(response2.data)
        
        assert response2.status_code == 200, "Second addition should succeed"
        assert len(data2['updated_cards']) > 0, "Should have updated cards on second addition"
        assert len(data2['added_cards']) == 0, "Should have no new cards on second addition"
        
        print(f"✓ Second addition: {data2['total_cards_modified']} cards modified")
        print(f"  New cards: {len(data2['added_cards'])}")
        print(f"  Updated cards: {len(data2['updated_cards'])}")
        
        # Verify quantities doubled
        with app.app_context():
            kid = UserCollection.query.filter_by(
                user_id=user_id,
                card_name='Eustass Kid'
            ).first()
            # ST-02 has Eustass Kid as leader (quantity 1), so after adding twice we should have 2
            assert kid.quantity == 2, f"Eustass Kid quantity should be 2, got {kid.quantity}"
            print(f"✓ Verified Eustass Kid quantity doubled: {kid.quantity}")

def test_invalid_structure_deck():
    """Test adding an invalid structure deck"""
    print("\n" + "="*60)
    print("Test 5: Add Invalid Structure Deck")
    print("="*60)
    
    setup_test_db()
    
    with app.test_client() as client:
        # Login
        client.post('/api/login', 
            json={'username': 'testuser', 'password': 'password123'},
            content_type='application/json'
        )
        
        # Try to add invalid deck
        response = client.post('/api/collection/add-structure-deck',
            json={'deck_code': 'ST-99'},
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        assert data['success'] == False, "Response should indicate failure"
        print(f"✓ Correctly rejected invalid deck code ST-99")

def main():
    """Run all tests"""
    print("="*60)
    print("Structure Deck Test Suite")
    print("="*60)
    
    try:
        test_get_structure_decks()
        test_get_structure_deck_details()
        test_add_structure_deck_to_collection()
        test_add_structure_deck_twice()
        test_invalid_structure_deck()
        
        print("\n" + "="*60)
        print("All Tests Passed! ✓")
        print("="*60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
