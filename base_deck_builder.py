"""
Base Deck Builder for Trading Card Games
This module provides an abstract base class that can be extended for any TCG
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import random


class BaseDeckBuilder(ABC):
    """Abstract base class for TCG deck builders"""
    
    def __init__(self, db_session=None):
        """Initialize the deck builder with card database"""
        self.db = db_session
        self.cards = None  # Will be loaded from database
        self.max_copies = 4  # Most TCGs use 4 as default
        self.max_deck_build_attempts = 1000
        self.max_improvement_attempts = 200
    
    @property
    @abstractmethod
    def deck_size(self) -> int:
        """Return the standard deck size for this TCG"""
        pass
    
    @property
    @abstractmethod
    def game_name(self) -> str:
        """Return the name of the TCG"""
        pass
    
    @property
    @abstractmethod
    def colors(self) -> List[str]:
        """Return the list of valid colors for this TCG"""
        pass
    
    @property
    @abstractmethod
    def card_types(self) -> List[str]:
        """Return the list of valid card types for this TCG"""
        pass
    
    @abstractmethod
    def _load_cards_from_db(self) -> List[Dict]:
        """Load all cards from the database for this specific TCG"""
        pass
    
    def get_all_cards(self) -> List[Dict]:
        """Return all available cards"""
        if self.cards is None:
            self.cards = self._load_cards_from_db()
        return self.cards
    
    @abstractmethod
    def build_deck(self, strategy: str = 'balanced', 
                   color: str = 'any', 
                   **kwargs) -> Dict:
        """
        Build a deck based on strategy and color preferences
        
        Args:
            strategy: Deck strategy (varies by TCG)
            color: Primary color
            **kwargs: Additional TCG-specific parameters
        
        Returns:
            Dictionary containing the built deck
        """
        pass
    
    def _calculate_type_distribution(self, strategy: str, has_leader: bool = True) -> Dict[str, float]:
        """
        Calculate the distribution of card types based on strategy
        
        Args:
            strategy: Deck strategy ('aggressive', 'balanced', 'control')
            has_leader: Whether this TCG uses leader cards
        
        Returns:
            Dictionary mapping card types to their percentage
        """
        if strategy == 'aggressive':
            return {'Character': 0.75, 'Event': 0.20, 'Stage': 0.05}
        elif strategy == 'control':
            return {'Character': 0.55, 'Event': 0.35, 'Stage': 0.10}
        else:  # balanced
            return {'Character': 0.65, 'Event': 0.30, 'Stage': 0.05}
    
    def _select_cards_by_distribution(self, available_cards: List[Dict], 
                                     distribution: Dict[str, float],
                                     target_count: int) -> List[Dict]:
        """
        Select cards according to type distribution
        
        Args:
            available_cards: Pool of cards to select from
            distribution: Desired distribution of card types
            target_count: Number of cards to select
        
        Returns:
            List of selected cards
        """
        selected = []
        cards_by_type = {}
        
        # Group cards by type
        for card in available_cards:
            card_type = card.get('type', 'Character')
            if card_type not in cards_by_type:
                cards_by_type[card_type] = []
            cards_by_type[card_type].append(card)
        
        # Calculate target count for each type
        for card_type, percentage in distribution.items():
            if card_type not in cards_by_type:
                continue
            
            type_count = int(target_count * percentage)
            type_cards = cards_by_type[card_type]
            
            # Select cards of this type
            while len([c for c in selected if c['type'] == card_type]) < type_count and type_cards:
                card = random.choice(type_cards)
                # Check if we haven't exceeded max copies
                card_count = len([c for c in selected if c['name'] == card['name']])
                if card_count < self.max_copies:
                    selected.append(card)
                else:
                    type_cards.remove(card)
        
        # Fill remaining slots with random cards
        while len(selected) < target_count and available_cards:
            card = random.choice(available_cards)
            card_count = len([c for c in selected if c['name'] == card['name']])
            if card_count < self.max_copies:
                selected.append(card)
        
        return selected
    
    def analyze_deck(self, deck: List[Dict]) -> Dict:
        """
        Analyze a deck and provide insights
        
        Args:
            deck: List of cards in the deck
        
        Returns:
            Dictionary containing analysis results
        """
        if not deck:
            return {
                'total_cards': 0,
                'suggestions': ['Deck is empty']
            }
        
        # Calculate statistics
        total_cards = len(deck)
        
        # Cost distribution
        cost_distribution = {}
        for card in deck:
            cost = card.get('cost', 0)
            cost_distribution[cost] = cost_distribution.get(cost, 0) + 1
        
        # Type distribution
        type_distribution = {}
        for card in deck:
            card_type = card.get('type', 'Unknown')
            type_distribution[card_type] = type_distribution.get(card_type, 0) + 1
        
        # Color distribution
        color_distribution = {}
        for card in deck:
            colors = card.get('colors', [])
            for color in colors:
                color_distribution[color] = color_distribution.get(color, 0) + 1
        
        # Calculate average cost
        total_cost = sum(card.get('cost', 0) for card in deck)
        avg_cost = total_cost / total_cards if total_cards > 0 else 0
        
        # Generate suggestions
        suggestions = []
        
        if total_cards < self.deck_size:
            suggestions.append(f'Deck has {total_cards} cards, needs {self.deck_size - total_cards} more')
        elif total_cards > self.deck_size:
            suggestions.append(f'Deck has {total_cards} cards, remove {total_cards - self.deck_size} cards')
        
        if avg_cost > 5:
            suggestions.append('Average cost is high - consider adding lower cost cards')
        elif avg_cost < 2.5:
            suggestions.append('Average cost is low - consider adding some higher impact cards')
        
        return {
            'total_cards': total_cards,
            'average_cost': round(avg_cost, 2),
            'cost_distribution': cost_distribution,
            'type_distribution': type_distribution,
            'color_distribution': color_distribution,
            'suggestions': suggestions if suggestions else ['Deck looks balanced!']
        }
