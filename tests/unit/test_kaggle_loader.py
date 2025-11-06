"""
Unit tests for Kaggle data loader
"""
import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
import csv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.services.kaggle_loader import KaggleDataLoader


def create_test_dataset(temp_dir):
    """Create a test dataset with sample CSV files"""
    
    # Create cards.csv
    cards_data = [
        {
            'name': 'Test Leader',
            'type': 'Leader',
            'colors': '["Red"]',
            'cost': 0,
            'power': 5000,
            'life': 5,
            'attribute': 'Strike',
            'effect': 'Test leader effect',
            'set': 'TEST01',
            'card_number': '001',
            'rarity': 'Leader',
            'image_url': 'https://example.com/test.png'
        },
        {
            'name': 'Test Character',
            'type': 'Character',
            'colors': '["Red", "Blue"]',
            'cost': 3,
            'power': 4000,
            'life': '',
            'attribute': 'Slash',
            'effect': 'Test character effect',
            'set': 'TEST01',
            'card_number': '002',
            'rarity': 'Common',
            'image_url': 'https://example.com/test2.png'
        },
        {
            'name': 'Test Event',
            'type': 'Event',
            'colors': '["Green"]',
            'cost': 2,
            'power': '',
            'life': '',
            'attribute': '',
            'effect': 'Test event effect',
            'set': 'TEST02',
            'card_number': '001',
            'rarity': 'Uncommon',
            'image_url': ''
        }
    ]
    
    cards_file = temp_dir / 'cards.csv'
    with open(cards_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=cards_data[0].keys())
        writer.writeheader()
        writer.writerows(cards_data)
    
    # Create sets.csv
    sets_data = [
        {
            'code': 'TEST01',
            'name': 'Test Set 1',
            'release_date': '2024-01-01'
        },
        {
            'code': 'TEST02',
            'name': 'Test Set 2',
            'release_date': '2024-02-01'
        }
    ]
    
    sets_file = temp_dir / 'sets.csv'
    with open(sets_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sets_data[0].keys())
        writer.writeheader()
        writer.writerows(sets_data)
    
    # Create structure_decks.csv
    decks_data = [
        {
            'code': 'ST-TEST',
            'name': 'Test Starter Deck',
            'description': 'A test starter deck',
            'color': 'Red',
            'leader': 'Test Leader',
            'cards': json.dumps({
                'Test Character': 4,
                'Test Event': 2
            })
        }
    ]
    
    decks_file = temp_dir / 'structure_decks.csv'
    with open(decks_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=decks_data[0].keys())
        writer.writeheader()
        writer.writerows(decks_data)


def test_kaggle_loader_initialization():
    """Test KaggleDataLoader initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        loader = KaggleDataLoader(data_dir=temp_dir)
        assert loader.data_dir == Path(temp_dir)
        assert loader.data_dir.exists()


def test_dataset_info():
    """Test getting dataset information"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        loader = KaggleDataLoader(data_dir=temp_dir)
        
        # Initially no files
        info = loader.get_dataset_info()
        assert info['files_exist'] == False
        assert len(info['files']) == 0
        
        # Create test dataset
        create_test_dataset(temp_path)
        
        # Now files should exist
        info = loader.get_dataset_info()
        assert info['files_exist'] == True
        assert 'cards.csv' in info['files']
        assert 'sets.csv' in info['files']
        assert 'structure_decks.csv' in info['files']


def test_load_cards():
    """Test loading cards from CSV"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        create_test_dataset(temp_path)
        
        loader = KaggleDataLoader(data_dir=temp_dir)
        cards, error = loader.load_cards()
        
        assert error is None
        assert len(cards) == 3
        
        # Check first card (Leader)
        leader = cards[0]
        assert leader['name'] == 'Test Leader'
        assert leader['type'] == 'Leader'
        assert leader['colors'] == ['Red']
        assert leader['cost'] == 0
        assert leader['power'] == 5000
        assert leader['life'] == 5
        assert leader['set'] == 'TEST01'
        assert leader['card_number'] == '001'
        
        # Check second card (Character)
        character = cards[1]
        assert character['name'] == 'Test Character'
        assert character['type'] == 'Character'
        assert character['colors'] == ['Red', 'Blue']
        assert character['cost'] == 3
        assert character['power'] == 4000
        assert character['life'] is None
        
        # Check third card (Event)
        event = cards[2]
        assert event['name'] == 'Test Event'
        assert event['type'] == 'Event'
        assert event['colors'] == ['Green']
        assert event['power'] is None


def test_load_expansions():
    """Test loading expansions/sets from CSV"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        create_test_dataset(temp_path)
        
        loader = KaggleDataLoader(data_dir=temp_dir)
        sets, error = loader.load_expansions()
        
        assert error is None
        assert len(sets) == 2
        
        # Check first set
        set1 = sets[0]
        assert set1['code'] == 'TEST01'
        assert set1['name'] == 'Test Set 1'
        assert set1['release_date'] == '2024-01-01'
        
        # Check second set
        set2 = sets[1]
        assert set2['code'] == 'TEST02'
        assert set2['name'] == 'Test Set 2'


def test_load_expansions_from_cards():
    """Test extracting sets from cards when sets.csv doesn't exist"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        create_test_dataset(temp_path)
        
        # Remove sets.csv
        (temp_path / 'sets.csv').unlink()
        
        loader = KaggleDataLoader(data_dir=temp_dir)
        sets, error = loader.load_expansions()
        
        assert error is None
        assert len(sets) == 2
        
        # Check that sets were extracted from cards
        set_codes = [s['code'] for s in sets]
        assert 'TEST01' in set_codes
        assert 'TEST02' in set_codes


def test_load_structure_decks():
    """Test loading structure decks from CSV"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        create_test_dataset(temp_path)
        
        loader = KaggleDataLoader(data_dir=temp_dir)
        decks, error = loader.load_structure_decks()
        
        assert error is None
        assert len(decks) == 1
        
        # Check deck
        deck = decks[0]
        assert deck['code'] == 'ST-TEST'
        assert deck['name'] == 'Test Starter Deck'
        assert deck['color'] == 'Red'
        assert deck['leader'] == 'Test Leader'
        assert 'Test Character' in deck['cards']
        assert deck['cards']['Test Character'] == 4


def test_parse_colors_various_formats():
    """Test color parsing with different input formats"""
    with tempfile.TemporaryDirectory() as temp_dir:
        loader = KaggleDataLoader(data_dir=temp_dir)
        
        # Test JSON array string
        assert loader._parse_colors('["Red", "Blue"]') == ['Red', 'Blue']
        
        # Test comma-separated
        assert loader._parse_colors('Red, Blue') == ['Red', 'Blue']
        
        # Test single color
        assert loader._parse_colors('Red') == ['Red']
        
        # Test list input
        assert loader._parse_colors(['Red', 'Blue']) == ['Red', 'Blue']
        
        # Test empty/None
        assert loader._parse_colors('') == []
        assert loader._parse_colors(None) == []


def test_load_cards_missing_file():
    """Test loading cards when file doesn't exist"""
    with tempfile.TemporaryDirectory() as temp_dir:
        loader = KaggleDataLoader(data_dir=temp_dir)
        cards, error = loader.load_cards()
        
        assert cards == []
        assert error is not None
        assert 'not found' in error.lower()


def test_load_structure_decks_missing_file():
    """Test loading structure decks when file doesn't exist"""
    with tempfile.TemporaryDirectory() as temp_dir:
        loader = KaggleDataLoader(data_dir=temp_dir)
        decks, error = loader.load_structure_decks()
        
        assert decks == []
        assert error is not None


if __name__ == '__main__':
    print("Running Kaggle loader tests...")
    
    test_kaggle_loader_initialization()
    print("✓ Test: Loader initialization")
    
    test_dataset_info()
    print("✓ Test: Dataset info")
    
    test_load_cards()
    print("✓ Test: Load cards")
    
    test_load_expansions()
    print("✓ Test: Load expansions")
    
    test_load_expansions_from_cards()
    print("✓ Test: Load expansions from cards")
    
    test_load_structure_decks()
    print("✓ Test: Load structure decks")
    
    test_parse_colors_various_formats()
    print("✓ Test: Parse colors in various formats")
    
    test_load_cards_missing_file()
    print("✓ Test: Handle missing cards file")
    
    test_load_structure_decks_missing_file()
    print("✓ Test: Handle missing structure decks file")
    
    print("\n✓ All tests passed!")
