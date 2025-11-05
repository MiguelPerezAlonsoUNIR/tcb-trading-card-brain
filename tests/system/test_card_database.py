#!/usr/bin/env python
"""
Test script for database-backed card storage system
Run this to verify card database operations
"""
import sys
import os

# Add the project root directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from app import app, db
from models import Card, CardSet
from deck_builder import OnePieceDeckBuilder
import json

def test_card_database():
    """Test card database operations"""
    print("=" * 60)
    print("Card Database System - Test Suite")
    print("=" * 60)
    
    # Set up test app context
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        # Drop all tables first to start fresh
        db.drop_all()
        # Create all tables
        db.create_all()
        
        # Test 1: Create Card Set
        print("\n" + "-" * 60)
        print("Test 1: Creating Card Set")
        print("-" * 60)
        
        card_set = CardSet(
            code='TEST01',
            name='Test Set'
        )
        db.session.add(card_set)
        db.session.commit()
        
        assert CardSet.query.count() == 1, "Card set not created"
        print(f"✓ Card set created: {card_set.code} - {card_set.name}")
        
        # Test 2: Create Card
        print("\n" + "-" * 60)
        print("Test 2: Creating Card")
        print("-" * 60)
        
        card = Card(
            name='Test Character',
            card_type='Character',
            power=5000,
            cost=4,
            attribute='Strike',
            effect='Test effect',
            set_id=card_set.id,
            card_number='001',
            rarity='Common'
        )
        card.set_colors(['Red', 'Blue'])
        db.session.add(card)
        db.session.commit()
        
        assert Card.query.count() == 1, "Card not created"
        print(f"✓ Card created: {card.name}")
        print(f"  - Type: {card.card_type}")
        print(f"  - Colors: {card.get_colors()}")
        print(f"  - Power: {card.power}")
        print(f"  - Cost: {card.cost}")
        
        # Test 3: Card to_dict() method
        print("\n" + "-" * 60)
        print("Test 3: Card Serialization")
        print("-" * 60)
        
        card_dict = card.to_dict()
        assert card_dict['name'] == 'Test Character', "Card name not serialized correctly"
        assert card_dict['type'] == 'Character', "Card type not serialized correctly"
        assert card_dict['colors'] == ['Red', 'Blue'], "Card colors not serialized correctly"
        assert card_dict['set'] == 'TEST01', "Card set not serialized correctly"
        print(f"✓ Card serialization works correctly")
        print(f"  Serialized card: {json.dumps(card_dict, indent=2)}")
        
        # Test 4: Query Cards by Type
        print("\n" + "-" * 60)
        print("Test 4: Querying Cards by Type")
        print("-" * 60)
        
        # Add more test cards
        leader = Card(
            name='Test Leader',
            card_type='Leader',
            power=5000,
            cost=0,
            life=5,
            attribute='Strike',
            effect='Leader effect',
            set_id=card_set.id,
            card_number='002',
            rarity='Leader'
        )
        leader.set_colors(['Red'])
        db.session.add(leader)
        
        event = Card(
            name='Test Event',
            card_type='Event',
            cost=2,
            effect='Event effect',
            set_id=card_set.id,
            card_number='003',
            rarity='Common'
        )
        event.set_colors(['Red'])
        db.session.add(event)
        
        db.session.commit()
        
        characters = Card.query.filter_by(card_type='Character').all()
        leaders = Card.query.filter_by(card_type='Leader').all()
        events = Card.query.filter_by(card_type='Event').all()
        
        assert len(characters) == 1, "Character query failed"
        assert len(leaders) == 1, "Leader query failed"
        assert len(events) == 1, "Event query failed"
        print(f"✓ Query by type works correctly")
        print(f"  - Characters: {len(characters)}")
        print(f"  - Leaders: {len(leaders)}")
        print(f"  - Events: {len(events)}")
        
        # Test 5: Update Card
        print("\n" + "-" * 60)
        print("Test 5: Updating Card")
        print("-" * 60)
        
        card.power = 6000
        card.effect = 'Updated effect'
        db.session.commit()
        
        updated_card = Card.query.get(card.id)
        assert updated_card.power == 6000, "Card power not updated"
        assert updated_card.effect == 'Updated effect', "Card effect not updated"
        print(f"✓ Card updated successfully")
        print(f"  - New power: {updated_card.power}")
        print(f"  - New effect: {updated_card.effect}")
        
        # Test 6: Deck Builder with Database
        print("\n" + "-" * 60)
        print("Test 6: Deck Builder Integration")
        print("-" * 60)
        
        # Add more cards to build a minimal deck
        for i in range(4, 20):
            new_card = Card(
                name=f'Test Character {i}',
                card_type='Character',
                power=3000 + (i * 100),
                cost=2 + (i % 5),
                attribute='Strike',
                effect=f'Effect {i}',
                set_id=card_set.id,
                card_number=f'{i:03d}',
                rarity='Common'
            )
            new_card.set_colors(['Red'])
            db.session.add(new_card)
        
        db.session.commit()
        
        # Test deck builder
        deck_builder = OnePieceDeckBuilder(db_session=db.session)
        cards = deck_builder.get_all_cards()
        
        assert len(cards) > 0, "Deck builder not loading cards from database"
        print(f"✓ Deck builder loads {len(cards)} cards from database")
        
        # Verify card types
        card_types = {}
        for c in cards:
            card_type = c['type']
            card_types[card_type] = card_types.get(card_type, 0) + 1
        
        print(f"  Card distribution:")
        for card_type, count in card_types.items():
            print(f"    - {card_type}: {count}")
        
        # Test 7: Delete Card
        print("\n" + "-" * 60)
        print("Test 7: Deleting Card")
        print("-" * 60)
        
        card_to_delete = Card.query.filter_by(card_number='019').first()
        if card_to_delete:
            card_name = card_to_delete.name
            db.session.delete(card_to_delete)
            db.session.commit()
            
            deleted_card = Card.query.filter_by(card_number='019').first()
            assert deleted_card is None, "Card not deleted"
            print(f"✓ Card deleted successfully: {card_name}")
        
        # Test 8: Unique Constraint
        print("\n" + "-" * 60)
        print("Test 8: Unique Constraint (Set + Card Number)")
        print("-" * 60)
        
        duplicate_card = Card(
            name='Duplicate Card',
            card_type='Character',
            power=5000,
            cost=4,
            set_id=card_set.id,
            card_number='001',  # Same as first card
            rarity='Common'
        )
        duplicate_card.set_colors(['Red'])
        db.session.add(duplicate_card)
        
        try:
            db.session.commit()
            print("✗ Unique constraint not enforced - duplicate card was added")
        except Exception as e:
            db.session.rollback()
            print(f"✓ Unique constraint enforced - duplicate card rejected")
        
        # Final Statistics
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        
        total_sets = CardSet.query.count()
        total_cards = Card.query.count()
        total_leaders = Card.query.filter_by(card_type='Leader').count()
        total_characters = Card.query.filter_by(card_type='Character').count()
        total_events = Card.query.filter_by(card_type='Event').count()
        
        print(f"\nDatabase Statistics:")
        print(f"  Total Card Sets: {total_sets}")
        print(f"  Total Cards: {total_cards}")
        print(f"    - Leaders: {total_leaders}")
        print(f"    - Characters: {total_characters}")
        print(f"    - Events: {total_events}")
        
        print("\n✓ All tests passed!")
        
        return True

if __name__ == '__main__':
    try:
        test_card_database()
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
