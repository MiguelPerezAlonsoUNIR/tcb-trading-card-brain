#!/usr/bin/env python
"""
Load card data from Kaggle dataset into the database

This script downloads the One Piece TCG card database from Kaggle and loads it into
the application database.

Usage:
    python load_kaggle_data.py [--download] [--force]
    
Options:
    --download    Download the dataset from Kaggle (requires Kaggle API credentials)
    --force       Force re-download even if dataset exists
    --info        Show dataset information without loading
    
Setup Kaggle API:
    1. Create a Kaggle account at https://www.kaggle.com
    2. Go to Account settings and create an API token
    3. Download kaggle.json and place it in ~/.kaggle/kaggle.json
    4. Or set environment variables KAGGLE_USERNAME and KAGGLE_KEY
    
For more information: https://github.com/Kaggle/kaggle-api
"""
import sys
import os
import argparse
import logging

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from src.models import db, Card, CardSet
from src.services.kaggle_loader import KaggleDataLoader

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def show_dataset_info(loader: KaggleDataLoader):
    """Display information about the dataset"""
    info = loader.get_dataset_info()
    
    print("\n" + "=" * 70)
    print("KAGGLE DATASET INFORMATION")
    print("=" * 70)
    print(f"Dataset: {info['dataset_name']}")
    print(f"Data Directory: {info['data_directory']}")
    print(f"Dataset Exists: {'Yes' if info['files_exist'] else 'No'}")
    
    if info['files']:
        print(f"\nFiles in directory:")
        for f in info['files']:
            print(f"  - {f}")
    else:
        print("\nNo files found. Use --download to download the dataset.")
    
    print("=" * 70)


def load_card_sets(loader: KaggleDataLoader) -> dict:
    """Load card sets from Kaggle dataset"""
    logger.info("Loading card sets from Kaggle dataset...")
    
    sets, error = loader.load_expansions()
    if error:
        logger.error(f"Failed to load sets: {error}")
        return {}
    
    set_id_map = {}
    sets_added = 0
    sets_skipped = 0
    
    for set_data in sets:
        set_code = set_data['code']
        
        # Check if set already exists
        card_set = CardSet.query.filter_by(code=set_code).first()
        if card_set:
            set_id_map[set_code] = card_set.id
            sets_skipped += 1
            continue
        
        # Create new card set
        card_set = CardSet(
            code=set_code,
            name=set_data['name'],
            release_date=None  # TODO: Parse release_date if available
        )
        db.session.add(card_set)
        db.session.flush()
        set_id_map[set_code] = card_set.id
        sets_added += 1
        logger.info(f"  ✓ Added card set: {set_code} - {set_data['name']}")
    
    db.session.commit()
    
    logger.info(f"Card sets loaded: {sets_added} added, {sets_skipped} skipped")
    return set_id_map


def load_cards(loader: KaggleDataLoader, set_id_map: dict):
    """Load cards from Kaggle dataset"""
    logger.info("Loading cards from Kaggle dataset...")
    
    cards, error = loader.load_cards()
    if error:
        logger.error(f"Failed to load cards: {error}")
        return
    
    cards_added = 0
    cards_skipped = 0
    cards_errors = 0
    
    for card_data in cards:
        try:
            set_code = card_data['set']
            card_number = card_data['card_number']
            
            # Get set_id
            set_id = set_id_map.get(set_code)
            if not set_id:
                logger.warning(f"  ⚠ Skipping card {card_data['name']} - set {set_code} not found")
                cards_errors += 1
                continue
            
            # Check if card already exists
            existing_card = Card.query.filter_by(set_id=set_id, card_number=card_number).first()
            if existing_card:
                cards_skipped += 1
                continue
            
            # Create new card
            card = Card(
                name=card_data['name'],
                card_type=card_data['type'],
                power=card_data.get('power'),
                cost=card_data.get('cost', 0),
                life=card_data.get('life'),
                attribute=card_data.get('attribute'),
                effect=card_data.get('effect'),
                set_id=set_id,
                card_number=card_number,
                rarity=card_data.get('rarity'),
                image_url=card_data.get('image_url')
            )
            
            # Set colors
            card.set_colors(card_data['colors'])
            
            db.session.add(card)
            cards_added += 1
            
            if cards_added % 50 == 0:
                db.session.commit()
                logger.info(f"  ... {cards_added} cards added")
        
        except Exception as e:
            logger.error(f"  ✗ Failed to add card {card_data.get('name', 'Unknown')}: {str(e)}")
            cards_errors += 1
    
    db.session.commit()
    
    logger.info(f"Cards loaded: {cards_added} added, {cards_skipped} skipped, {cards_errors} errors")


def load_structure_decks(loader: KaggleDataLoader):
    """Load structure decks from Kaggle dataset"""
    logger.info("Loading structure decks from Kaggle dataset...")
    
    decks, error = loader.load_structure_decks()
    if error:
        logger.warning(f"Structure decks not available: {error}")
        return
    
    # For now, just log the structure decks
    # In the future, we could add a StructureDeck model to the database
    logger.info(f"Found {len(decks)} structure decks")
    for deck in decks:
        logger.info(f"  - {deck['code']}: {deck['name']}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Load One Piece TCG data from Kaggle dataset',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--download', action='store_true', 
                       help='Download dataset from Kaggle')
    parser.add_argument('--force', action='store_true',
                       help='Force re-download even if dataset exists')
    parser.add_argument('--info', action='store_true',
                       help='Show dataset information only')
    parser.add_argument('--data-dir', type=str,
                       help='Custom data directory')
    
    args = parser.parse_args()
    
    # Initialize loader
    loader = KaggleDataLoader(data_dir=args.data_dir)
    
    # Show info and exit if requested
    if args.info:
        show_dataset_info(loader)
        return
    
    # Download dataset if requested
    if args.download:
        print("\n" + "=" * 70)
        print("DOWNLOADING DATASET FROM KAGGLE")
        print("=" * 70)
        success, error = loader.download_dataset(force=args.force)
        if not success:
            print(f"\n✗ Download failed: {error}")
            print("\nPlease ensure you have:")
            print("  1. A Kaggle account")
            print("  2. Kaggle API credentials configured")
            print("  3. See instructions above for setup")
            sys.exit(1)
        print("\n✓ Dataset downloaded successfully")
    
    # Check if dataset exists
    info = loader.get_dataset_info()
    if not info['files_exist']:
        print("\n✗ Dataset files not found.")
        print("\nPlease download the dataset first:")
        print("  python load_kaggle_data.py --download")
        sys.exit(1)
    
    # Load data into database
    print("\n" + "=" * 70)
    print("LOADING DATA INTO DATABASE")
    print("=" * 70)
    
    with app.app_context():
        # Create tables if they don't exist
        logger.info("Creating database tables...")
        db.create_all()
        
        # Load card sets
        set_id_map = load_card_sets(loader)
        
        # Load cards
        load_cards(loader, set_id_map)
        
        # Load structure decks (informational only for now)
        load_structure_decks(loader)
        
        # Print summary
        print("\n" + "=" * 70)
        print("DATABASE SUMMARY")
        print("=" * 70)
        
        total_sets = CardSet.query.count()
        total_cards = Card.query.count()
        total_leaders = Card.query.filter_by(card_type='Leader').count()
        total_characters = Card.query.filter_by(card_type='Character').count()
        total_events = Card.query.filter_by(card_type='Event').count()
        total_stages = Card.query.filter_by(card_type='Stage').count()
        
        print(f"\nTotal Card Sets: {total_sets}")
        print(f"Total Cards: {total_cards}")
        print(f"  - Leaders: {total_leaders}")
        print(f"  - Characters: {total_characters}")
        print(f"  - Events: {total_events}")
        print(f"  - Stages: {total_stages}")
        print("\n✓ Data loaded successfully!")
        print("=" * 70)


if __name__ == '__main__':
    main()
