"""
One Piece TCG Deck Builder AI Logic
This module contains the core deck building logic using AI
"""
import json
import random
from typing import List, Dict, Optional
from cards_data import ONEPIECE_CARDS, CARD_TYPES, COLORS

class OnePieceDeckBuilder:
    """AI-powered deck builder for One Piece TCG"""
    
    def __init__(self):
        """Initialize the deck builder with card database"""
        self.cards = ONEPIECE_CARDS
        self.deck_size = 50  # Standard One Piece TCG deck size
        self.max_copies = 4  # Maximum copies of a card (except for leaders)
        
    def get_all_cards(self) -> List[Dict]:
        """Return all available cards"""
        return self.cards
    
    def build_deck(self, strategy: str = 'balanced', 
                   color: str = 'any', 
                   leader: Optional[str] = None) -> Dict:
        """
        Build a deck based on strategy and color preferences
        
        Args:
            strategy: Deck strategy ('aggressive', 'balanced', 'control')
            color: Primary color ('red', 'blue', 'green', 'purple', 'black', 'yellow', 'any')
            leader: Specific leader card name (optional)
        
        Returns:
            Dictionary containing the built deck
        """
        deck = {
            'leader': None,
            'main_deck': [],
            'strategy': strategy,
            'color': color
        }
        
        # Step 1: Select leader
        leader_card = self._select_leader(color, leader)
        deck['leader'] = leader_card
        
        # Step 2: Build main deck based on strategy
        main_deck = self._build_main_deck(strategy, color, leader_card)
        deck['main_deck'] = main_deck
        
        return deck
    
    def _select_leader(self, color: str, leader_name: Optional[str]) -> Dict:
        """Select a leader card"""
        leaders = [c for c in self.cards if c['type'] == 'Leader']
        
        if leader_name:
            # Find specific leader
            for leader in leaders:
                if leader['name'].lower() == leader_name.lower():
                    return leader
        
        # Filter by color if specified
        if color != 'any':
            color_leaders = [l for l in leaders if color.lower() in [c.lower() for c in l['colors']]]
            if color_leaders:
                leaders = color_leaders
        
        # Select a random leader
        return random.choice(leaders) if leaders else leaders[0]
    
    def _build_main_deck(self, strategy: str, color: str, leader: Dict) -> List[Dict]:
        """Build the main deck based on strategy"""
        main_deck = []
        
        # Filter cards by color (matching leader's colors)
        available_cards = [
            c for c in self.cards 
            if c['type'] != 'Leader' and 
            (color == 'any' or any(lc in c['colors'] for lc in leader['colors']))
        ]
        
        # Strategy-based card selection
        if strategy == 'aggressive':
            main_deck = self._build_aggressive_deck(available_cards)
        elif strategy == 'control':
            main_deck = self._build_control_deck(available_cards)
        else:  # balanced
            main_deck = self._build_balanced_deck(available_cards)
        
        # Ensure deck is exactly 50 cards
        attempts = 0
        while len(main_deck) < self.deck_size and attempts < 200:
            if not available_cards:
                break
            card = random.choice(available_cards)
            if self._count_card_copies(main_deck, card) < self.max_copies:
                main_deck.append(card)
            attempts += 1
        
        # If we couldn't reach 50 cards with max copies, fill with any available cards
        if len(main_deck) < self.deck_size:
            all_non_leader_cards = [c for c in self.cards if c['type'] != 'Leader']
            attempts = 0
            while len(main_deck) < self.deck_size and attempts < 200:
                card = random.choice(all_non_leader_cards)
                if self._count_card_copies(main_deck, card) < self.max_copies:
                    main_deck.append(card)
                attempts += 1
        
        return main_deck[:self.deck_size]
    
    def _build_aggressive_deck(self, cards: List[Dict]) -> List[Dict]:
        """Build an aggressive deck focusing on low-cost, high-power characters"""
        deck = []
        
        # Prioritize characters with cost <= 5 and high power
        characters = [c for c in cards if c['type'] == 'Character' and c['cost'] <= 5]
        events = [c for c in cards if c['type'] == 'Event']
        
        # Add characters (70% of deck)
        attempts = 0
        while len(deck) < 35 and attempts < 100:
            if characters:
                card = random.choice(characters)
                if self._count_card_copies(deck, card) < self.max_copies:
                    deck.append(card)
            attempts += 1
        
        # Add events (30% of deck)
        attempts = 0
        while len(deck) < 50 and attempts < 100:
            if events:
                card = random.choice(events)
                if self._count_card_copies(deck, card) < self.max_copies:
                    deck.append(card)
            attempts += 1
        
        return deck
    
    def _build_control_deck(self, cards: List[Dict]) -> List[Dict]:
        """Build a control deck focusing on removal and high-cost characters"""
        deck = []
        
        # Prioritize events and high-cost characters
        events = [c for c in cards if c['type'] == 'Event']
        characters = [c for c in cards if c['type'] == 'Character' and c['cost'] >= 4]
        
        # Add events (40% of deck)
        attempts = 0
        while len(deck) < 20 and attempts < 100:
            if events:
                card = random.choice(events)
                if self._count_card_copies(deck, card) < self.max_copies:
                    deck.append(card)
            attempts += 1
        
        # Add characters (60% of deck)
        attempts = 0
        while len(deck) < 50 and attempts < 100:
            if characters:
                card = random.choice(characters)
                if self._count_card_copies(deck, card) < self.max_copies:
                    deck.append(card)
            attempts += 1
        
        return deck
    
    def _build_balanced_deck(self, cards: List[Dict]) -> List[Dict]:
        """Build a balanced deck with good mix of characters and events"""
        deck = []
        
        characters = [c for c in cards if c['type'] == 'Character']
        events = [c for c in cards if c['type'] == 'Event']
        stages = [c for c in cards if c['type'] == 'Stage']
        
        # Add characters (65% of deck)
        attempts = 0
        while len(deck) < 32 and attempts < 100:
            if characters:
                card = random.choice(characters)
                if self._count_card_copies(deck, card) < self.max_copies:
                    deck.append(card)
            attempts += 1
        
        # Add events (30% of deck)
        attempts = 0
        while len(deck) < 47 and attempts < 100:
            if events:
                card = random.choice(events)
                if self._count_card_copies(deck, card) < self.max_copies:
                    deck.append(card)
            attempts += 1
        
        # Add stages (5% of deck)
        attempts = 0
        while len(deck) < 50 and attempts < 100:
            if stages:
                card = random.choice(stages)
                if self._count_card_copies(deck, card) < self.max_copies:
                    deck.append(card)
            attempts += 1
        
        return deck
    
    def _count_card_copies(self, deck: List[Dict], card: Dict) -> int:
        """Count how many copies of a card are in the deck"""
        return sum(1 for c in deck if c['name'] == card['name'])
    
    def analyze_deck(self, deck: List[Dict]) -> Dict:
        """
        Analyze a deck and provide AI-powered suggestions
        
        Args:
            deck: List of cards in the deck
        
        Returns:
            Dictionary containing analysis and suggestions
        """
        analysis = {
            'total_cards': len(deck),
            'curve': self._analyze_cost_curve(deck),
            'type_distribution': self._analyze_type_distribution(deck),
            'color_distribution': self._analyze_color_distribution(deck),
            'suggestions': []
        }
        
        # Generate suggestions based on analysis
        if len(deck) != self.deck_size:
            analysis['suggestions'].append(
                f"Deck should have exactly {self.deck_size} cards. Current: {len(deck)}"
            )
        
        # Check cost curve
        avg_cost = sum(c.get('cost', 0) for c in deck) / len(deck) if deck else 0
        if avg_cost > 5:
            analysis['suggestions'].append(
                "Average cost is high. Consider adding more low-cost cards for better tempo."
            )
        elif avg_cost < 3:
            analysis['suggestions'].append(
                "Average cost is low. Consider adding some high-impact cards."
            )
        
        # Check type distribution
        type_dist = analysis['type_distribution']
        character_ratio = type_dist.get('Character', 0) / len(deck) if deck else 0
        if character_ratio < 0.5:
            analysis['suggestions'].append(
                "Low character count. Consider adding more characters to maintain board presence."
            )
        
        return analysis
    
    def _analyze_cost_curve(self, deck: List[Dict]) -> Dict:
        """Analyze the mana cost distribution"""
        curve = {}
        for card in deck:
            cost = card.get('cost', 0)
            curve[cost] = curve.get(cost, 0) + 1
        return curve
    
    def _analyze_type_distribution(self, deck: List[Dict]) -> Dict:
        """Analyze card type distribution"""
        distribution = {}
        for card in deck:
            card_type = card.get('type', 'Unknown')
            distribution[card_type] = distribution.get(card_type, 0) + 1
        return distribution
    
    def _analyze_color_distribution(self, deck: List[Dict]) -> Dict:
        """Analyze color distribution"""
        distribution = {}
        for card in deck:
            for color in card.get('colors', []):
                distribution[color] = distribution.get(color, 0) + 1
        return distribution
