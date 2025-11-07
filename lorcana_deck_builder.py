"""
Disney Lorcana TCG Deck Builder AI Logic
This module contains the core deck building logic for Disney Lorcana
"""
import json
import random
from typing import List, Dict, Optional
from base_deck_builder import BaseDeckBuilder


class LorcanaDeckBuilder(BaseDeckBuilder):
    """AI-powered deck builder for Disney Lorcana TCG"""
    
    @property
    def deck_size(self) -> int:
        """Lorcana decks have exactly 60 cards"""
        return 60
    
    @property
    def game_name(self) -> str:
        return "Disney Lorcana"
    
    @property
    def colors(self) -> List[str]:
        """Lorcana ink colors"""
        return ['Amber', 'Amethyst', 'Emerald', 'Ruby', 'Sapphire', 'Steel']
    
    @property
    def card_types(self) -> List[str]:
        """Lorcana card types"""
        return ['Character', 'Action', 'Item', 'Location']
    
    def _load_cards_from_db(self) -> List[Dict]:
        """Load all Lorcana cards from the database"""
        if self.db is None:
            # Fallback to sample cards if no database session provided
            return self._get_sample_lorcana_cards()
        
        from src.models import Card
        # Filter cards for Lorcana game
        cards = Card.query.filter_by(card_type='Lorcana').all()
        if not cards:
            # If no Lorcana cards in DB yet, return sample cards
            return self._get_sample_lorcana_cards()
        return [card.to_dict() for card in cards]
    
    def _get_sample_lorcana_cards(self) -> List[Dict]:
        """Get sample Lorcana cards for initial testing"""
        sample_cards = []
        
        # Sample characters for each color
        characters = [
            # Amber cards
            {'name': 'Simba - Protective Cub', 'type': 'Character', 'colors': ['Amber'], 'cost': 1, 'power': 1, 'effect': 'Challenger +2', 'inkable': True},
            {'name': 'Simba - Returned King', 'type': 'Character', 'colors': ['Amber'], 'cost': 7, 'power': 5, 'effect': 'Pounce', 'inkable': True},
            {'name': 'Heihei - Boat Snack', 'type': 'Character', 'colors': ['Amber'], 'cost': 2, 'power': 2, 'effect': 'Evasive', 'inkable': True},
            {'name': 'Tigger - Wonderful Thing About Tiggers', 'type': 'Character', 'colors': ['Amber'], 'cost': 4, 'power': 3, 'effect': 'Bounce', 'inkable': True},
            {'name': 'Flynn Rider - Charming Rogue', 'type': 'Character', 'colors': ['Amber'], 'cost': 3, 'power': 2, 'effect': 'Here Comes the Smolder', 'inkable': True},
            
            # Amethyst cards
            {'name': 'Maleficent - Monstrous Dragon', 'type': 'Character', 'colors': ['Amethyst'], 'cost': 8, 'power': 6, 'effect': 'Dragon Fire', 'inkable': True},
            {'name': 'Dr. Facilier - Remarkable Gentleman', 'type': 'Character', 'colors': ['Amethyst'], 'cost': 3, 'power': 2, 'effect': 'Read the Cards', 'inkable': True},
            {'name': 'Ursula - Power Hungry', 'type': 'Character', 'colors': ['Amethyst'], 'cost': 5, 'power': 3, 'effect': 'Divination', 'inkable': True},
            {'name': 'Maleficent - Sinister Visitor', 'type': 'Character', 'colors': ['Amethyst'], 'cost': 2, 'power': 2, 'effect': 'Forbidden Curse', 'inkable': True},
            {'name': 'Yzma - Alchemist', 'type': 'Character', 'colors': ['Amethyst'], 'cost': 4, 'power': 3, 'effect': 'Lab Coat', 'inkable': True},
            
            # Emerald cards
            {'name': 'Rapunzel - Gifted with Healing', 'type': 'Character', 'colors': ['Emerald'], 'cost': 5, 'power': 4, 'effect': 'Gleam and Glow', 'inkable': True},
            {'name': 'Tinker Bell - Giant Fairy', 'type': 'Character', 'colors': ['Emerald'], 'cost': 6, 'power': 5, 'effect': 'Pixie Dust', 'inkable': True},
            {'name': 'Cinderella - Stouthearted', 'type': 'Character', 'colors': ['Emerald'], 'cost': 4, 'power': 3, 'effect': 'A Wonderful Dream', 'inkable': True},
            {'name': 'Robin Hood - Unrivaled Archer', 'type': 'Character', 'colors': ['Emerald'], 'cost': 3, 'power': 3, 'effect': 'Merry Men', 'inkable': True},
            {'name': 'Peter Pan - Never Landing', 'type': 'Character', 'colors': ['Emerald'], 'cost': 2, 'power': 2, 'effect': 'Flying', 'inkable': True},
            
            # Ruby cards
            {'name': 'Aladdin - Heroic Outlaw', 'type': 'Character', 'colors': ['Ruby'], 'cost': 4, 'power': 3, 'effect': 'Street Rat', 'inkable': True},
            {'name': 'Mulan - Imperial Soldier', 'type': 'Character', 'colors': ['Ruby'], 'cost': 3, 'power': 3, 'effect': 'Battlefield Tactics', 'inkable': True},
            {'name': 'Gaston - Arrogant Hunter', 'type': 'Character', 'colors': ['Ruby'], 'cost': 5, 'power': 4, 'effect': 'Challenge', 'inkable': True},
            {'name': 'Beast - Relentless', 'type': 'Character', 'colors': ['Ruby'], 'cost': 6, 'power': 5, 'effect': 'Roar', 'inkable': True},
            {'name': 'Hercules - True Hero', 'type': 'Character', 'colors': ['Ruby'], 'cost': 7, 'power': 6, 'effect': 'Heroic Strength', 'inkable': True},
            
            # Sapphire cards
            {'name': 'Elsa - Spirit of Winter', 'type': 'Character', 'colors': ['Sapphire'], 'cost': 5, 'power': 4, 'effect': 'Deep Freeze', 'inkable': True},
            {'name': 'Mickey Mouse - Wayward Sorcerer', 'type': 'Character', 'colors': ['Sapphire'], 'cost': 2, 'power': 1, 'effect': 'Animate Broom', 'inkable': True},
            {'name': 'Merlin - Goat', 'type': 'Character', 'colors': ['Sapphire'], 'cost': 1, 'power': 1, 'effect': 'Bounce', 'inkable': True},
            {'name': 'Genie - On the Job', 'type': 'Character', 'colors': ['Sapphire'], 'cost': 4, 'power': 2, 'effect': 'Phenomenal Cosmic Power', 'inkable': True},
            {'name': 'Archimedes - Highly Educated Owl', 'type': 'Character', 'colors': ['Sapphire'], 'cost': 3, 'power': 2, 'effect': 'Knowledge is Power', 'inkable': True},
            
            # Steel cards
            {'name': 'Stitch - Rock Star', 'type': 'Character', 'colors': ['Steel'], 'cost': 6, 'power': 5, 'effect': 'Performance', 'inkable': True},
            {'name': 'Donald Duck - Boisterous Fowl', 'type': 'Character', 'colors': ['Steel'], 'cost': 2, 'power': 2, 'effect': 'Lose Temper', 'inkable': True},
            {'name': 'Captain Hook - Forceful Duelist', 'type': 'Character', 'colors': ['Steel'], 'cost': 4, 'power': 4, 'effect': 'Bodyguard', 'inkable': True},
            {'name': 'Mufasa - Betrayed Leader', 'type': 'Character', 'colors': ['Steel'], 'cost': 5, 'power': 4, 'effect': 'Stampede', 'inkable': True},
            {'name': 'Scar - Mastermind', 'type': 'Character', 'colors': ['Steel'], 'cost': 3, 'power': 2, 'effect': 'Prepared', 'inkable': True},
        ]
        
        # Add some actions and items
        actions_items = [
            # Actions
            {'name': 'Stampede', 'type': 'Action', 'colors': ['Amber'], 'cost': 3, 'effect': 'Deal 2 damage to chosen character', 'inkable': True},
            {'name': 'Be Prepared', 'type': 'Action', 'colors': ['Amethyst'], 'cost': 2, 'effect': 'Draw 2 cards', 'inkable': True},
            {'name': 'Healing Glow', 'type': 'Action', 'colors': ['Emerald'], 'cost': 2, 'effect': 'Remove up to 3 damage from chosen character', 'inkable': True},
            {'name': 'Fan the Flames', 'type': 'Action', 'colors': ['Ruby'], 'cost': 1, 'effect': 'Ready chosen character', 'inkable': True},
            {'name': 'Freeze', 'type': 'Action', 'colors': ['Sapphire'], 'cost': 3, 'effect': 'Exert chosen opposing character', 'inkable': True},
            {'name': 'Break', 'type': 'Action', 'colors': ['Steel'], 'cost': 2, 'effect': 'Banish chosen item', 'inkable': True},
            
            # Items
            {'name': 'Maurice\'s Workshop', 'type': 'Item', 'colors': ['Amber'], 'cost': 3, 'effect': 'Whenever you play a character, you may pay 1 ink to draw a card', 'inkable': True},
            {'name': 'Scepter of Arendelle', 'type': 'Item', 'colors': ['Sapphire'], 'cost': 4, 'effect': 'Your characters with cost 5 or more gain Evasive', 'inkable': True},
            {'name': 'Magic Mirror', 'type': 'Item', 'colors': ['Amethyst'], 'cost': 2, 'effect': 'Look at the top 2 cards of your deck', 'inkable': True},
            {'name': 'Fishbone Quill', 'type': 'Item', 'colors': ['Emerald'], 'cost': 1, 'effect': 'When you play this item, draw a card', 'inkable': True},
        ]
        
        sample_cards.extend(characters)
        sample_cards.extend(actions_items)
        
        # Add set and card number info
        for i, card in enumerate(sample_cards):
            card['set'] = 'TFC'  # The First Chapter
            card['card_number'] = str(i + 1)
            card['rarity'] = 'Common' if i % 3 == 0 else 'Uncommon'
            card['image_url'] = None
        
        return sample_cards
    
    def build_deck(self, strategy: str = 'balanced', 
                   color: str = 'any', 
                   **kwargs) -> Dict:
        """
        Build a Lorcana deck based on strategy and color preferences
        
        Args:
            strategy: Deck strategy ('aggressive', 'balanced', 'control')
            color: Primary ink color ('Amber', 'Amethyst', 'Emerald', 'Ruby', 'Sapphire', 'Steel', 'any')
            **kwargs: Additional parameters (unused for Lorcana)
        
        Returns:
            Dictionary containing the built deck
        """
        deck = {
            'main_deck': [],
            'strategy': strategy,
            'color': color,
            'game': self.game_name
        }
        
        # Build 60-card deck (no leader in Lorcana)
        main_deck = self._build_main_deck(strategy, color)
        deck['main_deck'] = main_deck
        
        return deck
    
    def _build_main_deck(self, strategy: str, color: str) -> List[Dict]:
        """Build the main deck for Lorcana"""
        cards = self.get_all_cards()
        
        # Filter by color if specified
        if color != 'any':
            available_cards = [
                c for c in cards 
                if color in c.get('colors', [])
            ]
        else:
            available_cards = cards
        
        if not available_cards:
            # Fallback to all cards if no matches
            available_cards = cards
        
        # Lorcana type distribution (Characters, Actions, Items, Locations)
        if strategy == 'aggressive':
            distribution = {'Character': 0.70, 'Action': 0.20, 'Item': 0.10}
        elif strategy == 'control':
            distribution = {'Character': 0.50, 'Action': 0.30, 'Item': 0.15, 'Location': 0.05}
        else:  # balanced
            distribution = {'Character': 0.60, 'Action': 0.25, 'Item': 0.15}
        
        main_deck = self._select_cards_by_distribution(
            available_cards, 
            distribution, 
            self.deck_size
        )
        
        return main_deck
    
    def build_deck_from_collection(self, strategy: str = 'balanced',
                                  color: str = 'any',
                                  owned_cards: Dict[str, int] = None) -> Dict:
        """
        Build a Lorcana deck prioritizing cards from the user's collection
        
        Args:
            strategy: Deck strategy
            color: Primary color
            owned_cards: Dictionary mapping card names to quantities owned
        
        Returns:
            Dictionary containing the built deck with collection info
        """
        if owned_cards is None:
            owned_cards = {}
        
        # Build deck normally
        deck = self.build_deck(strategy, color)
        
        # Calculate which cards the user owns
        owned_count = 0
        needed_cards = []
        
        for card in deck['main_deck']:
            card_name = card['name']
            if card_name in owned_cards and owned_cards[card_name] > 0:
                owned_count += 1
            else:
                needed_cards.append(card_name)
        
        deck['collection_info'] = {
            'owned_cards': owned_count,
            'total_cards': len(deck['main_deck']),
            'percentage_owned': round(owned_count / len(deck['main_deck']) * 100, 1) if deck['main_deck'] else 0,
            'needed_cards': list(set(needed_cards))
        }
        
        return deck
    
    def suggest_improvements(self, deck: Dict, owned_cards: Dict[str, int] = None) -> Dict:
        """
        Suggest improvements for an existing Lorcana deck
        
        Args:
            deck: Current deck
            owned_cards: Dictionary of cards owned by user
        
        Returns:
            Dictionary with improvement suggestions
        """
        if owned_cards is None:
            owned_cards = {}
        
        improvements = {
            'balanced': None,
            'aggressive': None,
            'control': None
        }
        
        strategy = deck.get('strategy', 'balanced')
        color = deck.get('color', 'any')
        
        # Generate three variations
        for improvement_type in improvements.keys():
            improved_deck = self.build_deck(
                strategy=improvement_type,
                color=color
            )
            
            # Add collection info
            if owned_cards:
                owned_count = sum(1 for card in improved_deck['main_deck'] 
                                if card['name'] in owned_cards)
                improved_deck['collection_coverage'] = {
                    'owned': owned_count,
                    'total': len(improved_deck['main_deck']),
                    'percentage': round(owned_count / len(improved_deck['main_deck']) * 100, 1)
                }
            
            improvements[improvement_type] = {
                'deck': improved_deck,
                'description': self._get_improvement_description(improvement_type)
            }
        
        return improvements
    
    def _get_improvement_description(self, strategy: str) -> str:
        """Get description for improvement strategy"""
        descriptions = {
            'balanced': 'Optimized for versatile gameplay with a mix of characters, actions, and items',
            'aggressive': 'Optimized for fast gameplay with low-cost characters and quick actions',
            'control': 'Optimized for late-game dominance with powerful effects and control actions'
        }
        return descriptions.get(strategy, 'Optimized deck')
