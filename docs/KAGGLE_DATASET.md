# Kaggle Dataset Integration

This document explains how to use the Kaggle dataset integration to load One Piece TCG card data, expansions, and structure decks.

## Overview

The TCB Trading Card Brain now supports loading card data from the comprehensive [One Piece TCG Card Database on Kaggle](https://www.kaggle.com/datasets/jbowski/one-piece-tcg-card-database). This dataset provides:

- **Card Data**: Complete card information including stats, effects, and images
- **Expansions**: All card sets and their release information
- **Structure Decks**: Pre-built starter and structure deck lists

## Prerequisites

### 1. Install Dependencies

The Kaggle integration requires additional Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- `kaggle`: Official Kaggle API client
- `pandas`: Data processing library

### 2. Setup Kaggle API Credentials

To download datasets from Kaggle, you need API credentials:

#### Step 1: Create a Kaggle Account
Visit [kaggle.com](https://www.kaggle.com) and create a free account if you don't have one.

#### Step 2: Generate API Token
1. Go to your Kaggle account settings: https://www.kaggle.com/settings
2. Scroll down to the "API" section
3. Click "Create New Token"
4. This will download a `kaggle.json` file

#### Step 3: Install Credentials

**Option A: Using kaggle.json file (Recommended)**
```bash
# Linux/Mac
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Windows (PowerShell)
mkdir $env:USERPROFILE\.kaggle
move Downloads\kaggle.json $env:USERPROFILE\.kaggle\
```

**Option B: Using Environment Variables**
```bash
export KAGGLE_USERNAME=your_username
export KAGGLE_KEY=your_api_key
```

For more details, see the [Kaggle API documentation](https://github.com/Kaggle/kaggle-api).

## Usage

### Check Dataset Information

Before downloading, you can check if the dataset is already available:

```bash
python load_kaggle_data.py --info
```

This will show:
- Dataset name and location
- Whether files exist locally
- List of available files

### Download Dataset from Kaggle

To download the dataset from Kaggle:

```bash
python load_kaggle_data.py --download
```

Options:
- `--download`: Download the dataset from Kaggle
- `--force`: Force re-download even if files exist
- `--data-dir <path>`: Use a custom directory for dataset files

Example with custom directory:
```bash
python load_kaggle_data.py --download --data-dir /path/to/data
```

### Load Data into Database

Once the dataset is downloaded, load it into the database:

```bash
python load_kaggle_data.py
```

This will:
1. Create database tables if they don't exist
2. Load card sets/expansions
3. Load all cards with their complete information
4. Load structure deck definitions
5. Display a summary of loaded data

### Load from Existing Dataset Files

If you already have the dataset CSV files locally:

1. Create the data directory:
```bash
mkdir -p data/kaggle
```

2. Place the CSV files in the directory:
   - `cards.csv`: Card data
   - `sets.csv`: Expansion/set data (optional)
   - `structure_decks.csv`: Structure deck data (optional)

3. Run the loader:
```bash
python load_kaggle_data.py
```

## Dataset Structure

### Cards Data (cards.csv)

Expected columns:
- `name`: Card name
- `type` or `card_type`: Card type (Leader, Character, Event, Stage)
- `colors` or `color`: Card colors (comma-separated or JSON array)
- `cost`: Cost to play
- `power`: Power value (for Characters and Leaders)
- `life`: Life value (for Leaders)
- `attribute`: Card attribute (Strike, Slash, Special, etc.)
- `effect`: Card effect text
- `set` or `set_code`: Set code (e.g., "OP01", "ST01")
- `card_number` or `number`: Card number within set
- `rarity`: Rarity level
- `image_url` or `image`: URL to card image

### Sets Data (sets.csv)

Expected columns:
- `code` or `set_code`: Unique set code
- `name` or `set_name`: Set name
- `release_date`: Release date (optional)

### Structure Decks Data (structure_decks.csv)

Expected columns:
- `code` or `deck_code`: Deck code (e.g., "ST-01")
- `name` or `deck_name`: Deck name
- `description`: Deck description
- `color`: Main color
- `leader`: Leader card name
- `cards` or `card_list`: Card list (JSON format)

## Integration with Application

### Using Kaggle Data in the Application

Once loaded, the data is available through the standard Card and CardSet models:

```python
from src.models import Card, CardSet

# Get all cards
cards = Card.query.all()

# Get all sets
sets = CardSet.query.all()

# Get cards from a specific set
op01_cards = Card.query.join(CardSet).filter(CardSet.code == 'OP01').all()
```

### Programmatic Access to Kaggle Loader

You can also use the KaggleDataLoader directly in your code:

```python
from src.services.kaggle_loader import KaggleDataLoader

loader = KaggleDataLoader()

# Download dataset
success, error = loader.download_dataset()

# Load cards
cards, error = loader.load_cards()

# Load expansions
expansions, error = loader.load_expansions()

# Load structure decks
decks, error = loader.load_structure_decks()

# Get dataset info
info = loader.get_dataset_info()
```

## Benefits of Using Kaggle Dataset

1. **Comprehensive Data**: Access to complete, up-to-date card information
2. **Community Maintained**: Dataset is maintained by the Kaggle community
3. **Structured Format**: Consistent CSV format for easy processing
4. **Regular Updates**: Dataset can be updated with new releases
5. **Offline Access**: Once downloaded, no internet required for loading data

## Troubleshooting

### "Could not find kaggle.json" Error

**Solution**: Ensure you have set up Kaggle API credentials as described in the Prerequisites section.

### "Dataset files not found" Error

**Solution**: Run with `--download` flag to download the dataset first:
```bash
python load_kaggle_data.py --download
```

### Permission Errors

**Solution**: Ensure the kaggle.json file has correct permissions:
```bash
chmod 600 ~/.kaggle/kaggle.json
```

### Missing Columns in CSV

**Solution**: The loader is flexible and tries multiple column name variations. Check the CSV file structure and ensure it has the basic required fields: name, type, set, card_number.

## Comparison with Legacy Data

The application maintains backward compatibility with the legacy `cards_data.py` file. You can use either:

- **Legacy approach**: `python init_cards_db.py` - Uses hardcoded data
- **Kaggle approach**: `python load_kaggle_data.py` - Uses Kaggle dataset

The Kaggle approach is recommended for:
- Larger datasets
- Regular updates
- Complete card information
- Community-maintained data

## Future Enhancements

Planned improvements:
- Automatic dataset updates
- Incremental loading (only load new/changed cards)
- Structure deck model in database
- Image caching from Kaggle dataset
- Data validation and error reporting

## Support

For issues or questions:
- Check the [Kaggle dataset page](https://www.kaggle.com/datasets/jbowski/one-piece-tcg-card-database)
- Review the [Kaggle API documentation](https://github.com/Kaggle/kaggle-api)
- Open an issue on the GitHub repository
