"""
Database models for user authentication and deck management
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    decks = db.relationship('Deck', backref='owner', lazy=True, cascade='all, delete-orphan')
    collection = db.relationship('UserCollection', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Deck(db.Model):
    """Deck model for storing user decks"""
    __tablename__ = 'decks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    strategy = db.Column(db.String(50))
    color = db.Column(db.String(50))
    leader_data = db.Column(db.Text)  # JSON string
    main_deck_data = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_leader(self, leader_dict):
        """Store leader as JSON string"""
        self.leader_data = json.dumps(leader_dict)
    
    def get_leader(self):
        """Retrieve leader from JSON string"""
        return json.loads(self.leader_data) if self.leader_data else None
    
    def set_main_deck(self, cards_list):
        """Store main deck as JSON string"""
        self.main_deck_data = json.dumps(cards_list)
    
    def get_main_deck(self):
        """Retrieve main deck from JSON string"""
        return json.loads(self.main_deck_data) if self.main_deck_data else []
    
    def to_dict(self):
        """Convert deck to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'strategy': self.strategy,
            'color': self.color,
            'leader': self.get_leader(),
            'main_deck': self.get_main_deck(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Deck {self.name} by User {self.user_id}>'

class UserCollection(db.Model):
    """User's card collection for deck suggestions"""
    __tablename__ = 'user_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    card_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate cards per user
    __table_args__ = (
        db.UniqueConstraint('user_id', 'card_name', name='unique_user_card'),
    )
    
    def __repr__(self):
        return f'<UserCollection User {self.user_id}: {self.card_name} x{self.quantity}>'

class CardSet(db.Model):
    """Card set/expansion information"""
    __tablename__ = 'card_sets'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)  # e.g., "OP01", "ST01"
    name = db.Column(db.String(200), nullable=False)  # e.g., "Romance Dawn", "Straw Hat Crew"
    release_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cards = db.relationship('Card', backref='card_set', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert card set to dictionary"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<CardSet {self.code}: {self.name}>'

class Card(db.Model):
    """Trading card information
    
    Note: Colors are stored as JSON strings for simplicity. For production systems with
    large datasets, consider using SQLAlchemy's JSON column type or a many-to-many
    relationship table for better query performance and normalization.
    """
    __tablename__ = 'cards'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    card_type = db.Column(db.String(50), nullable=False, index=True)  # Leader, Character, Event, Stage
    colors = db.Column(db.String(200), nullable=False)  # JSON array as string, e.g., '["Red", "Blue"]'
    power = db.Column(db.Integer, nullable=True)  # Power for Characters and Leaders
    cost = db.Column(db.Integer, nullable=False, default=0)
    life = db.Column(db.Integer, nullable=True)  # Life for Leaders
    attribute = db.Column(db.String(50), nullable=True)  # Strike, Slash, Special, etc.
    effect = db.Column(db.Text, nullable=True)
    set_id = db.Column(db.Integer, db.ForeignKey('card_sets.id'), nullable=False, index=True)
    card_number = db.Column(db.String(20), nullable=False)  # Card number within set
    rarity = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint for set + card number combination
    __table_args__ = (
        db.UniqueConstraint('set_id', 'card_number', name='unique_set_card'),
    )
    
    def get_colors(self):
        """Get colors as a list"""
        return json.loads(self.colors) if self.colors else []
    
    def set_colors(self, color_list):
        """Set colors from a list"""
        self.colors = json.dumps(color_list)
    
    def to_dict(self):
        """Convert card to dictionary matching the existing card format"""
        card_dict = {
            'id': self.id,
            'name': self.name,
            'type': self.card_type,
            'colors': self.get_colors(),
            'cost': self.cost,
            'effect': self.effect,
            'set': self.card_set.code if self.card_set else None,
            'card_number': self.card_number,
            'rarity': self.rarity,
            'image_url': self.image_url,
        }
        
        # Add optional fields if present
        if self.power is not None:
            card_dict['power'] = self.power
        if self.life is not None:
            card_dict['life'] = self.life
        if self.attribute:
            card_dict['attribute'] = self.attribute
            
        return card_dict
    
    def __repr__(self):
        return f'<Card {self.name} ({self.card_set.code if self.card_set else "?"}-{self.card_number})>'
