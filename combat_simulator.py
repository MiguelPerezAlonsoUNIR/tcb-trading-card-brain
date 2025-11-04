"""
Combat Simulator for One Piece TCG
AI-powered combat simulation that learns from tournament match data
"""
import random
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class TournamentMatch:
    """Represents a tournament match result for AI learning"""
    deck1_strategy: str
    deck1_color: str
    deck1_avg_cost: float
    deck1_character_ratio: float
    deck2_strategy: str
    deck2_color: str
    deck2_avg_cost: float
    deck2_character_ratio: float
    deck1_wins: bool
    match_duration: int  # Number of turns


# Tournament match data for AI learning
# Based on hypothetical tournament results
TOURNAMENT_DATA = [
    # Aggressive vs Control matchups
    TournamentMatch('aggressive', 'Red', 3.2, 0.70, 'control', 'Blue', 5.5, 0.60, True, 8),
    TournamentMatch('aggressive', 'Red', 3.0, 0.72, 'control', 'Blue', 5.8, 0.58, True, 7),
    TournamentMatch('aggressive', 'Green', 3.5, 0.68, 'control', 'Purple', 6.0, 0.55, False, 12),
    TournamentMatch('aggressive', 'Yellow', 3.3, 0.71, 'control', 'Black', 5.7, 0.57, True, 9),
    
    # Balanced vs Aggressive matchups
    TournamentMatch('balanced', 'Blue', 4.2, 0.65, 'aggressive', 'Red', 3.1, 0.70, True, 10),
    TournamentMatch('balanced', 'Purple', 4.5, 0.63, 'aggressive', 'Red', 3.0, 0.72, True, 11),
    TournamentMatch('balanced', 'Green', 4.3, 0.64, 'aggressive', 'Yellow', 3.4, 0.69, False, 8),
    
    # Balanced vs Control matchups
    TournamentMatch('balanced', 'Red', 4.0, 0.66, 'control', 'Blue', 5.6, 0.59, False, 14),
    TournamentMatch('balanced', 'Green', 4.4, 0.62, 'control', 'Purple', 5.9, 0.56, True, 13),
    TournamentMatch('balanced', 'Yellow', 4.1, 0.65, 'control', 'Black', 5.4, 0.61, False, 15),
    
    # Control vs Control matchups
    TournamentMatch('control', 'Blue', 5.7, 0.58, 'control', 'Purple', 5.5, 0.60, True, 18),
    TournamentMatch('control', 'Black', 5.8, 0.57, 'control', 'Blue', 5.6, 0.59, False, 20),
    
    # Aggressive vs Aggressive matchups
    TournamentMatch('aggressive', 'Red', 3.1, 0.71, 'aggressive', 'Green', 3.3, 0.69, True, 6),
    TournamentMatch('aggressive', 'Yellow', 3.2, 0.70, 'aggressive', 'Red', 3.0, 0.72, False, 7),
    
    # Same color matchups
    TournamentMatch('balanced', 'Red', 4.0, 0.66, 'aggressive', 'Red', 3.0, 0.72, False, 9),
    TournamentMatch('control', 'Blue', 5.6, 0.59, 'balanced', 'Blue', 4.2, 0.65, True, 14),
]


class CombatSimulator:
    """AI-powered combat simulator that learns from tournament data"""
    
    def __init__(self):
        """Initialize the combat simulator with tournament learning data"""
        self.tournament_data = TOURNAMENT_DATA
        
    def simulate_combat(self, deck1: Dict, deck2: Dict, num_simulations: int = 1000) -> Dict:
        """
        Simulate combat between two decks using AI learning
        
        Args:
            deck1: First deck with leader and main_deck
            deck2: Second deck with leader and main_deck
            num_simulations: Number of simulations to run (default 1000)
        
        Returns:
            Dictionary containing simulation results and statistics
        """
        # Extract deck characteristics
        deck1_stats = self._extract_deck_stats(deck1)
        deck2_stats = self._extract_deck_stats(deck2)
        
        # Calculate base win probability using AI learning
        base_win_rate = self._calculate_win_probability(deck1_stats, deck2_stats)
        
        # Run Monte Carlo simulations with variance
        wins = 0
        win_turns = []
        loss_turns = []
        
        for _ in range(num_simulations):
            # Add realistic variance to each simulation
            variance = random.gauss(0, 0.1)  # 10% standard deviation
            simulation_win_rate = max(0.0, min(1.0, base_win_rate + variance))
            
            if random.random() < simulation_win_rate:
                wins += 1
                # Estimate turn count for wins
                turn_count = self._estimate_turn_count(deck1_stats, deck2_stats, True)
                win_turns.append(turn_count)
            else:
                turn_count = self._estimate_turn_count(deck1_stats, deck2_stats, False)
                loss_turns.append(turn_count)
        
        # Calculate statistics
        win_rate = (wins / num_simulations) * 100
        avg_win_turns = sum(win_turns) / len(win_turns) if win_turns else 0
        avg_loss_turns = sum(loss_turns) / len(loss_turns) if loss_turns else 0
        
        # Generate insights
        insights = self._generate_insights(deck1_stats, deck2_stats, win_rate)
        
        # Key matchup analysis
        key_cards = self._identify_key_cards(deck1, deck2)
        
        return {
            'win_rate': round(win_rate, 2),
            'wins': wins,
            'losses': num_simulations - wins,
            'simulations_run': num_simulations,
            'avg_win_turns': round(avg_win_turns, 1),
            'avg_loss_turns': round(avg_loss_turns, 1),
            'insights': insights,
            'key_cards': key_cards,
            'deck1_stats': deck1_stats,
            'deck2_stats': deck2_stats,
            'matchup_type': self._get_matchup_type(deck1_stats, deck2_stats)
        }
    
    def _extract_deck_stats(self, deck: Dict) -> Dict:
        """Extract relevant statistics from a deck"""
        main_deck = deck.get('main_deck', [])
        strategy = deck.get('strategy', 'balanced')
        
        if not main_deck:
            return {
                'strategy': strategy,
                'color': 'any',
                'avg_cost': 4.0,
                'character_ratio': 0.65,
                'total_cards': 0
            }
        
        # Calculate average cost
        total_cost = sum(card.get('cost', 0) for card in main_deck)
        avg_cost = total_cost / len(main_deck) if main_deck else 4.0
        
        # Calculate character ratio
        character_count = sum(1 for card in main_deck if card.get('type') == 'Character')
        character_ratio = character_count / len(main_deck) if main_deck else 0.65
        
        # Determine primary color
        color_counts = {}
        for card in main_deck:
            for color in card.get('colors', []):
                color_counts[color] = color_counts.get(color, 0) + 1
        
        primary_color = max(color_counts.items(), key=lambda x: x[1])[0] if color_counts else 'any'
        
        return {
            'strategy': strategy,
            'color': primary_color,
            'avg_cost': avg_cost,
            'character_ratio': character_ratio,
            'total_cards': len(main_deck)
        }
    
    def _calculate_win_probability(self, deck1_stats: Dict, deck2_stats: Dict) -> float:
        """
        Calculate win probability using AI learning from tournament data
        """
        # Find similar matchups in tournament data
        similar_matches = []
        
        for match in self.tournament_data:
            similarity_score = self._calculate_matchup_similarity(
                deck1_stats, deck2_stats, match
            )
            if similarity_score > 0.5:  # Only consider reasonably similar matches
                similar_matches.append((match, similarity_score))
        
        if not similar_matches:
            # No similar matches found, use base probability
            return self._calculate_base_probability(deck1_stats, deck2_stats)
        
        # Weight tournament results by similarity
        weighted_wins = 0
        total_weight = 0
        
        for match, similarity in similar_matches:
            weight = similarity
            total_weight += weight
            if match.deck1_wins:
                weighted_wins += weight
        
        learned_probability = weighted_wins / total_weight if total_weight > 0 else 0.5
        
        # Blend learned probability with base calculation (70% learned, 30% base)
        base_probability = self._calculate_base_probability(deck1_stats, deck2_stats)
        final_probability = (learned_probability * 0.7) + (base_probability * 0.3)
        
        return max(0.1, min(0.9, final_probability))  # Clamp between 10% and 90%
    
    def _calculate_matchup_similarity(self, deck1_stats: Dict, deck2_stats: Dict, 
                                     match: TournamentMatch) -> float:
        """Calculate how similar a tournament match is to the current matchup"""
        similarity = 0.0
        
        # Strategy similarity (40% weight)
        if deck1_stats['strategy'] == match.deck1_strategy:
            similarity += 0.2
        if deck2_stats['strategy'] == match.deck2_strategy:
            similarity += 0.2
        
        # Cost curve similarity (30% weight)
        cost_diff1 = abs(deck1_stats['avg_cost'] - match.deck1_avg_cost)
        cost_diff2 = abs(deck2_stats['avg_cost'] - match.deck2_avg_cost)
        cost_similarity = max(0, 1 - (cost_diff1 + cost_diff2) / 6.0)
        similarity += cost_similarity * 0.3
        
        # Character ratio similarity (20% weight)
        ratio_diff1 = abs(deck1_stats['character_ratio'] - match.deck1_character_ratio)
        ratio_diff2 = abs(deck2_stats['character_ratio'] - match.deck2_character_ratio)
        ratio_similarity = max(0, 1 - (ratio_diff1 + ratio_diff2) / 0.4)
        similarity += ratio_similarity * 0.2
        
        # Color similarity (10% weight)
        if deck1_stats['color'] == match.deck1_color:
            similarity += 0.05
        if deck2_stats['color'] == match.deck2_color:
            similarity += 0.05
        
        return similarity
    
    def _calculate_base_probability(self, deck1_stats: Dict, deck2_stats: Dict) -> float:
        """Calculate base win probability using strategy matchup matrix"""
        # Strategy matchup advantages
        matchup_matrix = {
            ('aggressive', 'control'): 0.58,  # Aggressive beats Control
            ('control', 'balanced'): 0.55,     # Control beats Balanced
            ('balanced', 'aggressive'): 0.54,  # Balanced beats Aggressive
            ('aggressive', 'aggressive'): 0.50,
            ('balanced', 'balanced'): 0.50,
            ('control', 'control'): 0.50,
            ('control', 'aggressive'): 0.42,
            ('balanced', 'control'): 0.45,
            ('aggressive', 'balanced'): 0.46,
        }
        
        matchup_key = (deck1_stats['strategy'], deck2_stats['strategy'])
        base_prob = matchup_matrix.get(matchup_key, 0.50)
        
        # Adjust for cost curve
        cost_advantage = (deck2_stats['avg_cost'] - deck1_stats['avg_cost']) * 0.02
        
        # Adjust for character ratio (higher is generally better for board presence)
        character_advantage = (deck1_stats['character_ratio'] - deck2_stats['character_ratio']) * 0.15
        
        final_prob = base_prob + cost_advantage + character_advantage
        
        return max(0.1, min(0.9, final_prob))
    
    def _estimate_turn_count(self, deck1_stats: Dict, deck2_stats: Dict, 
                            deck1_wins: bool) -> int:
        """Estimate how many turns a match would take"""
        base_turns = 10
        
        # Aggressive decks end games faster
        if deck1_stats['strategy'] == 'aggressive' or deck2_stats['strategy'] == 'aggressive':
            base_turns -= 2
        
        # Control decks extend games
        if deck1_stats['strategy'] == 'control' and deck2_stats['strategy'] == 'control':
            base_turns += 6
        elif deck1_stats['strategy'] == 'control' or deck2_stats['strategy'] == 'control':
            base_turns += 3
        
        # Add some randomness
        variance = random.randint(-2, 2)
        return max(5, base_turns + variance)
    
    def _generate_insights(self, deck1_stats: Dict, deck2_stats: Dict, 
                          win_rate: float) -> List[str]:
        """Generate AI insights about the matchup"""
        insights = []
        
        # Win rate assessment
        if win_rate >= 65:
            insights.append("🟢 Strong Advantage: Your deck has a significant edge in this matchup")
        elif win_rate >= 55:
            insights.append("🟡 Slight Advantage: Your deck is favored but the match is winnable for both sides")
        elif win_rate >= 45:
            insights.append("⚪ Even Matchup: This is a very balanced matchup between the decks")
        elif win_rate >= 35:
            insights.append("🟡 Slight Disadvantage: The opponent is favored but you can win with good plays")
        else:
            insights.append("🔴 Difficult Matchup: This is a challenging matchup that requires excellent execution")
        
        # Strategy-specific insights
        if deck1_stats['strategy'] == 'aggressive' and deck2_stats['strategy'] == 'control':
            insights.append("⚡ Speed Advantage: Your aggressive strategy can outpace their control setup")
        elif deck1_stats['strategy'] == 'control' and deck2_stats['strategy'] == 'aggressive':
            insights.append("🛡️ Survivability Key: Focus on board clears and high-cost finishers")
        elif deck1_stats['strategy'] == 'balanced' and deck2_stats['strategy'] == 'aggressive':
            insights.append("⚖️ Flexibility: Your balanced approach can adapt to their aggressive plays")
        
        # Cost curve insights
        cost_diff = deck1_stats['avg_cost'] - deck2_stats['avg_cost']
        if cost_diff > 1.5:
            insights.append("📊 Cost Concern: Your higher average cost may struggle in the early game")
        elif cost_diff < -1.5:
            insights.append("⚡ Early Game Edge: Your lower cost curve gives you early board control")
        
        # Character ratio insights
        if deck1_stats['character_ratio'] > 0.70:
            insights.append("👥 Strong Board Presence: High character count provides excellent board control")
        elif deck1_stats['character_ratio'] < 0.55:
            insights.append("🎯 Event-Heavy: Make sure to maximize value from your event cards")
        
        return insights
    
    def _identify_key_cards(self, deck1: Dict, deck2: Dict) -> Dict:
        """Identify key cards that will impact the matchup"""
        main_deck = deck1.get('main_deck', [])
        
        # Find high-impact cards
        key_cards = {
            'high_power': [],
            'low_cost': [],
            'events': []
        }
        
        for card in main_deck:
            # High power characters (7000+)
            if card.get('type') == 'Character' and card.get('power', 0) >= 7000:
                if len(key_cards['high_power']) < 3:
                    key_cards['high_power'].append(card['name'])
            
            # Low cost threats (cost <= 2)
            if card.get('cost', 999) <= 2 and card.get('power', 0) >= 4000:
                if len(key_cards['low_cost']) < 3:
                    key_cards['low_cost'].append(card['name'])
            
            # Event cards
            if card.get('type') == 'Event':
                if len(key_cards['events']) < 3:
                    key_cards['events'].append(card['name'])
        
        return key_cards
    
    def _get_matchup_type(self, deck1_stats: Dict, deck2_stats: Dict) -> str:
        """Determine the type of matchup"""
        s1 = deck1_stats['strategy']
        s2 = deck2_stats['strategy']
        
        if s1 == s2:
            return f"Mirror Match ({s1.title()} vs {s2.title()})"
        else:
            return f"{s1.title()} vs {s2.title()}"
    
    def get_available_opponent_decks(self) -> List[Dict]:
        """Get a list of pre-built opponent decks for simulation"""
        # This could be expanded to load from a database of tournament decks
        return [
            {
                'id': 'opp_1',
                'name': 'Tournament Red Aggro',
                'strategy': 'aggressive',
                'color': 'Red',
                'description': 'Fast-paced red deck focusing on early board control',
                'avg_cost': 3.1,
                'win_rate': 62.5  # Tournament win rate
            },
            {
                'id': 'opp_2',
                'name': 'Blue Control Master',
                'strategy': 'control',
                'color': 'Blue',
                'description': 'Patient control deck with powerful late-game finishers',
                'avg_cost': 5.6,
                'win_rate': 58.3
            },
            {
                'id': 'opp_3',
                'name': 'Balanced Green Machine',
                'strategy': 'balanced',
                'color': 'Green',
                'description': 'Well-rounded green deck with versatile options',
                'avg_cost': 4.3,
                'win_rate': 55.0
            },
            {
                'id': 'opp_4',
                'name': 'Purple Control Elite',
                'strategy': 'control',
                'color': 'Purple',
                'description': 'High-cost purple control with devastating effects',
                'avg_cost': 5.9,
                'win_rate': 56.7
            },
            {
                'id': 'opp_5',
                'name': 'Yellow Rush',
                'strategy': 'aggressive',
                'color': 'Yellow',
                'description': 'Lightning-fast yellow aggro deck',
                'avg_cost': 3.3,
                'win_rate': 59.2
            }
        ]
