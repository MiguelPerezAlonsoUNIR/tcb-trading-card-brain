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
