#!/usr/bin/env python
"""
Test script for authentication and user features
Run this to verify authentication, deck management, and collection tracking
"""
import sys
import os

# Add the project root directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from app import app
from src.models import db, User, Deck, UserCollection
from src.services import AuthService
import json

def test_authentication():
    """Test authentication features"""
    print("=" * 60)
    print("Authentication & User Features - Test Suite")
    print("=" * 60)
    
    # Set up test app context
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        # Drop all tables first to start fresh
        db.drop_all()
        # Create all tables
        db.create_all()
        
        # Test 1: Password Hashing
        print("\n" + "-" * 60)
        print("Test 1: Password Hashing and Verification")
        print("-" * 60)
        password = "test_password_123"
        hashed = AuthService.hash_password(password)
        print(f"✓ Password hashed successfully")
        
        # Verify correct password
        assert AuthService.verify_password(password, hashed), "Password verification failed"
        print(f"✓ Correct password verified")
        
        # Verify incorrect password
        assert not AuthService.verify_password("wrong_password", hashed), "Wrong password accepted"
        print(f"✓ Incorrect password rejected")
        
        # Test 2: User Creation
        print("\n" + "-" * 60)
        print("Test 2: User Creation")
        print("-" * 60)
        user = User(
            username="testuser",
            password_hash=AuthService.hash_password("testpass123")
        )
        db.session.add(user)
        db.session.commit()
        print(f"✓ User created: {user.username} (ID: {user.id})")
        
        # Test 3: User Query
        print("\n" + "-" * 60)
        print("Test 3: User Query")
        print("-" * 60)
        queried_user = User.query.filter_by(username="testuser").first()
        assert queried_user is not None, "User not found"
        assert queried_user.username == "testuser", "Username mismatch"
        print(f"✓ User queried successfully: {queried_user.username}")
        
        # Test 4: Deck Creation
        print("\n" + "-" * 60)
        print("Test 4: Deck Creation and Storage")
        print("-" * 60)
        leader_data = {
            'name': 'Monkey D. Luffy',
            'type': 'Leader',
            'colors': ['Red'],
            'power': 5000
        }
        main_deck_data = [
            {'name': 'Card 1', 'type': 'Character', 'cost': 3},
            {'name': 'Card 2', 'type': 'Event', 'cost': 2}
        ]
        
        deck = Deck(
            user_id=user.id,
            name="Test Deck 1",
            strategy="balanced",
            color="Red"
        )
        deck.set_leader(leader_data)
        deck.set_main_deck(main_deck_data)
        db.session.add(deck)
        db.session.commit()
        print(f"✓ Deck created: {deck.name} (ID: {deck.id})")
        
        # Test 5: Deck Retrieval
        print("\n" + "-" * 60)
        print("Test 5: Deck Retrieval and JSON Parsing")
        print("-" * 60)
        retrieved_deck = Deck.query.filter_by(id=deck.id).first()
        assert retrieved_deck is not None, "Deck not found"
        retrieved_leader = retrieved_deck.get_leader()
        retrieved_main = retrieved_deck.get_main_deck()
        assert retrieved_leader['name'] == 'Monkey D. Luffy', "Leader data mismatch"
        assert len(retrieved_main) == 2, "Main deck size mismatch"
        print(f"✓ Deck retrieved: {retrieved_deck.name}")
        print(f"  Leader: {retrieved_leader['name']}")
        print(f"  Main deck: {len(retrieved_main)} cards")
        
        # Test 6: User Collection
        print("\n" + "-" * 60)
        print("Test 6: User Collection Management")
        print("-" * 60)
        collection_item = UserCollection(
            user_id=user.id,
            card_name="Monkey D. Luffy",
            quantity=2
        )
        db.session.add(collection_item)
        db.session.commit()
        print(f"✓ Collection item added: {collection_item.card_name} x{collection_item.quantity}")
        
        # Test 7: Collection Query
        print("\n" + "-" * 60)
        print("Test 7: Collection Query")
        print("-" * 60)
        user_collection = UserCollection.query.filter_by(user_id=user.id).all()
        assert len(user_collection) == 1, "Collection size mismatch"
        assert user_collection[0].card_name == "Monkey D. Luffy", "Card name mismatch"
        print(f"✓ Collection queried: {len(user_collection)} items")
        
        # Test 8: User Relationships
        print("\n" + "-" * 60)
        print("Test 8: User Relationships")
        print("-" * 60)
        user_decks = user.decks
        assert len(user_decks) == 1, "User decks relationship failed"
        user_coll = user.collection
        assert len(user_coll) == 1, "User collection relationship failed"
        print(f"✓ User has {len(user_decks)} deck(s)")
        print(f"✓ User has {len(user_coll)} collection item(s)")
        
        # Test 9: Multiple Users
        print("\n" + "-" * 60)
        print("Test 9: Multiple Users Isolation")
        print("-" * 60)
        user2 = User(
            username="testuser2",
            password_hash=AuthService.hash_password("testpass456")
        )
        db.session.add(user2)
        db.session.commit()
        
        deck2 = Deck(
            user_id=user2.id,
            name="User 2 Deck",
            strategy="aggressive",
            color="Blue"
        )
        deck2.set_leader(leader_data)
        deck2.set_main_deck(main_deck_data)
        db.session.add(deck2)
        db.session.commit()
        
        # Verify isolation
        user1_decks = Deck.query.filter_by(user_id=user.id).all()
        user2_decks = Deck.query.filter_by(user_id=user2.id).all()
        assert len(user1_decks) == 1, "User 1 has wrong number of decks"
        assert len(user2_decks) == 1, "User 2 has wrong number of decks"
        assert user1_decks[0].name != user2_decks[0].name, "Deck names should differ"
        print(f"✓ User 1 decks: {len(user1_decks)}")
        print(f"✓ User 2 decks: {len(user2_decks)}")
        print(f"✓ User data properly isolated")
        
        # Test 10: Deck Update
        print("\n" + "-" * 60)
        print("Test 10: Deck Update")
        print("-" * 60)
        original_name = deck.name
        deck.name = "Updated Test Deck"
        db.session.commit()
        updated_deck = Deck.query.filter_by(id=deck.id).first()
        assert updated_deck.name == "Updated Test Deck", "Deck name not updated"
        print(f"✓ Deck name updated: '{original_name}' -> '{updated_deck.name}'")
        
        # Test 11: Deck Deletion
        print("\n" + "-" * 60)
        print("Test 11: Deck Deletion")
        print("-" * 60)
        deck_id = deck2.id
        db.session.delete(deck2)
        db.session.commit()
        deleted_deck = Deck.query.filter_by(id=deck_id).first()
        assert deleted_deck is None, "Deck not deleted"
        print(f"✓ Deck deleted successfully")
        
        # Summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        print("✓ All authentication tests passed!")
        print("✓ User management working correctly")
        print("✓ Deck storage and retrieval working")
        print("✓ Collection tracking working")
        print("=" * 60)

if __name__ == '__main__':
    test_authentication()
