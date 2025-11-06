# Data Directory

This directory is used to store downloaded datasets and data files.

## Kaggle Dataset

The `kaggle/` subdirectory will be created automatically when you download the One Piece TCG dataset from Kaggle using:

```bash
python load_kaggle_data.py --download
```

### Expected Files

After downloading the Kaggle dataset, the following files will be available in `data/kaggle/`:

- `cards.csv` - Complete card database
- `sets.csv` - Card sets/expansions (optional)
- `structure_decks.csv` - Structure deck definitions (optional)

### Manual Dataset Placement

If you have the dataset files locally, you can place them in `data/kaggle/` manually:

1. Create the directory:
```bash
mkdir -p data/kaggle
```

2. Copy your CSV files:
```bash
cp /path/to/cards.csv data/kaggle/
cp /path/to/sets.csv data/kaggle/
cp /path/to/structure_decks.csv data/kaggle/
```

3. Load the data:
```bash
python load_kaggle_data.py
```

## CSV Format Examples

### cards.csv

```csv
name,type,colors,cost,power,life,attribute,effect,set,card_number,rarity,image_url
Monkey D. Luffy,Leader,"[""Red""]",0,5000,5,Strike,Your Characters gain +1000 power,ST01,001,Leader,https://example.com/card.png
Roronoa Zoro,Character,"[""Red""]",3,4000,,Slash,DON!! -1: This Character gains +1000 power,ST01,002,Common,https://example.com/card.png
```

### sets.csv

```csv
code,name,release_date
ST01,Straw Hat Crew,2024-01-01
OP01,Romance Dawn,2024-02-01
```

### structure_decks.csv

```csv
code,name,description,color,leader,cards
ST-01,Straw Hat Crew Starter,Red deck featuring Luffy,Red,Monkey D. Luffy,"{""Roronoa Zoro"": 4, ""Nami"": 4}"
```

## Notes

- The `data/` directory is gitignored to prevent committing large datasets
- CSV files can have flexible column names (e.g., both `colors` and `color` are supported)
- Leading zeros in card numbers are preserved
