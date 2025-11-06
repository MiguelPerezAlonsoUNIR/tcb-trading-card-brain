"""
Kaggle Dataset Loader Service
Loads card data, expansions, and structured decks from the Kaggle One Piece TCG dataset
Dataset: https://www.kaggle.com/datasets/jbowski/one-piece-tcg-card-database
"""
import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)


class KaggleDataLoader:
    """Service for loading One Piece TCG data from Kaggle dataset"""
    
    DATASET_NAME = "jbowski/one-piece-tcg-card-database"
    DATA_DIR = "data/kaggle"
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the Kaggle data loader
        
        Args:
            data_dir: Optional custom directory for dataset files
        """
        self.data_dir = Path(data_dir) if data_dir else Path(self.DATA_DIR)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def download_dataset(self, force: bool = False) -> Tuple[bool, Optional[str]]:
        """
        Download the dataset from Kaggle
        
        Args:
            force: Force re-download even if files exist
            
        Returns:
            (success, error_message)
        """
        try:
            import kaggle
            
            # Check if dataset already exists
            if not force and self._dataset_exists():
                logger.info("Dataset already exists. Use force=True to re-download.")
                return True, None
            
            logger.info(f"Downloading dataset {self.DATASET_NAME}...")
            kaggle.api.dataset_download_files(
                self.DATASET_NAME,
                path=str(self.data_dir),
                unzip=True
            )
            logger.info("Dataset downloaded successfully")
            return True, None
            
        except Exception as e:
            error_msg = f"Failed to download dataset: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def _dataset_exists(self) -> bool:
        """Check if dataset files exist"""
        expected_files = ['cards.csv', 'sets.csv', 'structure_decks.csv']
        return all((self.data_dir / f).exists() for f in expected_files)
    
    def load_cards(self) -> Tuple[List[Dict], Optional[str]]:
        """
        Load card data from the dataset
        
        Returns:
            (cards_list, error_message)
        """
        try:
            cards_file = self.data_dir / 'cards.csv'
            if not cards_file.exists():
                return [], f"Cards file not found: {cards_file}"
            
            logger.info(f"Loading cards from {cards_file}")
            # Read CSV with card_number and number as strings to preserve leading zeros
            df = pd.read_csv(cards_file, dtype={'card_number': str, 'number': str})
            
            cards = []
            for _, row in df.iterrows():
                card = self._parse_card_row(row)
                if card:
                    cards.append(card)
            
            logger.info(f"Loaded {len(cards)} cards from dataset")
            return cards, None
            
        except Exception as e:
            error_msg = f"Failed to load cards: {str(e)}"
            logger.error(error_msg)
            return [], error_msg
    
    def _parse_card_row(self, row: pd.Series) -> Optional[Dict]:
        """
        Parse a card row from the CSV into a card dictionary
        
        Args:
            row: Pandas Series containing card data
            
        Returns:
            Card dictionary or None if invalid
        """
        try:
            # Handle colors - might be comma-separated or JSON
            colors = self._parse_colors(row.get('colors', row.get('color', '')))
            
            card = {
                'name': str(row.get('name', '')).strip(),
                'type': str(row.get('type', row.get('card_type', 'Character'))).strip(),
                'colors': colors,
                'cost': int(row.get('cost', 0)) if pd.notna(row.get('cost')) else 0,
                'power': int(row.get('power', 0)) if pd.notna(row.get('power')) and row.get('power') != '' else None,
                'life': int(row.get('life', 0)) if pd.notna(row.get('life')) and row.get('life') != '' else None,
                'attribute': str(row.get('attribute', '')).strip() if pd.notna(row.get('attribute')) else None,
                'effect': str(row.get('effect', '')).strip() if pd.notna(row.get('effect')) else None,
                'set': str(row.get('set', row.get('set_code', ''))).strip(),
                'card_number': str(row.get('card_number', row.get('number', ''))).strip(),
                'rarity': str(row.get('rarity', '')).strip() if pd.notna(row.get('rarity')) else None,
                'image_url': str(row.get('image_url', row.get('image', ''))).strip() if pd.notna(row.get('image_url', row.get('image', ''))) else None
            }
            
            # Validate required fields
            if not card['name'] or not card['set'] or not card['card_number']:
                logger.warning(f"Skipping card with missing required fields: {row.to_dict()}")
                return None
            
            return card
            
        except Exception as e:
            logger.warning(f"Failed to parse card row: {str(e)}")
            return None
    
    def _parse_colors(self, color_value) -> List[str]:
        """
        Parse color value which might be a string, list, or JSON
        
        Args:
            color_value: Color data in various formats
            
        Returns:
            List of color strings
        """
        # If it's already a list, return it directly
        if isinstance(color_value, list):
            return [str(c).strip() for c in color_value]
        
        # Check for None or NaN
        if color_value is None or (isinstance(color_value, str) and color_value == ''):
            return []
        
        try:
            if pd.isna(color_value):
                return []
        except (ValueError, TypeError):
            # pd.isna can fail on certain types, just continue
            pass
        
        # Convert to string
        color_str = str(color_value).strip()
        
        # Try parsing as JSON
        if color_str.startswith('[') or color_str.startswith('{'):
            try:
                parsed = json.loads(color_str)
                if isinstance(parsed, list):
                    return [str(c).strip() for c in parsed]
                return [str(parsed).strip()]
            except json.JSONDecodeError:
                pass
        
        # Try comma-separated values
        if ',' in color_str:
            return [c.strip() for c in color_str.split(',') if c.strip()]
        
        # Single color
        return [color_str] if color_str else []
    
    def load_expansions(self) -> Tuple[List[Dict], Optional[str]]:
        """
        Load expansion/set data from the dataset
        
        Returns:
            (expansions_list, error_message)
        """
        try:
            sets_file = self.data_dir / 'sets.csv'
            if not sets_file.exists():
                logger.warning(f"Sets file not found: {sets_file}")
                # Try to extract sets from cards
                return self._extract_sets_from_cards()
            
            logger.info(f"Loading sets from {sets_file}")
            df = pd.read_csv(sets_file)
            
            sets = []
            for _, row in df.iterrows():
                set_data = {
                    'code': str(row.get('code', row.get('set_code', ''))).strip(),
                    'name': str(row.get('name', row.get('set_name', ''))).strip(),
                    'release_date': str(row.get('release_date', '')).strip() if pd.notna(row.get('release_date')) else None
                }
                
                if set_data['code']:
                    sets.append(set_data)
            
            logger.info(f"Loaded {len(sets)} sets from dataset")
            return sets, None
            
        except Exception as e:
            error_msg = f"Failed to load sets: {str(e)}"
            logger.error(error_msg)
            return [], error_msg
    
    def _extract_sets_from_cards(self) -> Tuple[List[Dict], Optional[str]]:
        """Extract unique sets from card data"""
        cards, error = self.load_cards()
        if error:
            return [], error
        
        sets_dict = {}
        for card in cards:
            set_code = card.get('set', '')
            if set_code and set_code not in sets_dict:
                sets_dict[set_code] = {
                    'code': set_code,
                    'name': f'Set {set_code}',
                    'release_date': None
                }
        
        sets = list(sets_dict.values())
        logger.info(f"Extracted {len(sets)} unique sets from cards")
        return sets, None
    
    def load_structure_decks(self) -> Tuple[List[Dict], Optional[str]]:
        """
        Load structure deck data from the dataset
        
        Returns:
            (decks_list, error_message)
        """
        try:
            decks_file = self.data_dir / 'structure_decks.csv'
            if not decks_file.exists():
                logger.warning(f"Structure decks file not found: {decks_file}")
                return [], f"Structure decks file not found: {decks_file}"
            
            logger.info(f"Loading structure decks from {decks_file}")
            df = pd.read_csv(decks_file)
            
            decks = []
            for _, row in df.iterrows():
                deck = self._parse_deck_row(row)
                if deck:
                    decks.append(deck)
            
            logger.info(f"Loaded {len(decks)} structure decks from dataset")
            return decks, None
            
        except Exception as e:
            error_msg = f"Failed to load structure decks: {str(e)}"
            logger.error(error_msg)
            return [], error_msg
    
    def _parse_deck_row(self, row: pd.Series) -> Optional[Dict]:
        """
        Parse a structure deck row from the CSV
        
        Args:
            row: Pandas Series containing deck data
            
        Returns:
            Deck dictionary or None if invalid
        """
        try:
            # Parse card list (might be JSON or comma-separated)
            cards_data = row.get('cards', row.get('card_list', ''))
            cards = self._parse_deck_cards(cards_data)
            
            deck = {
                'code': str(row.get('code', row.get('deck_code', ''))).strip(),
                'name': str(row.get('name', row.get('deck_name', ''))).strip(),
                'description': str(row.get('description', '')).strip() if pd.notna(row.get('description')) else '',
                'color': str(row.get('color', '')).strip() if pd.notna(row.get('color')) else None,
                'leader': str(row.get('leader', '')).strip() if pd.notna(row.get('leader')) else None,
                'cards': cards
            }
            
            if not deck['code'] or not deck['name']:
                logger.warning(f"Skipping deck with missing required fields: {row.to_dict()}")
                return None
            
            return deck
            
        except Exception as e:
            logger.warning(f"Failed to parse deck row: {str(e)}")
            return None
    
    def _parse_deck_cards(self, cards_data) -> Dict[str, int]:
        """
        Parse deck card list which might be JSON or other format
        
        Args:
            cards_data: Card list data in various formats
            
        Returns:
            Dictionary of card_name -> quantity
        """
        if pd.isna(cards_data) or cards_data == '':
            return {}
        
        cards_str = str(cards_data).strip()
        
        # Try parsing as JSON
        if cards_str.startswith('{') or cards_str.startswith('['):
            try:
                parsed = json.loads(cards_str)
                if isinstance(parsed, dict):
                    return {k: int(v) for k, v in parsed.items()}
                elif isinstance(parsed, list):
                    # Convert list to dict with quantities
                    result = {}
                    for item in parsed:
                        if isinstance(item, dict):
                            name = item.get('name', '')
                            qty = item.get('quantity', 1)
                            if name:
                                result[name] = int(qty)
                    return result
            except json.JSONDecodeError:
                pass
        
        return {}
    
    def get_dataset_info(self) -> Dict:
        """
        Get information about the downloaded dataset
        
        Returns:
            Dictionary with dataset information
        """
        info = {
            'dataset_name': self.DATASET_NAME,
            'data_directory': str(self.data_dir.absolute()),
            'files_exist': self._dataset_exists(),
            'files': []
        }
        
        if self.data_dir.exists():
            info['files'] = [f.name for f in self.data_dir.iterdir() if f.is_file()]
        
        return info
