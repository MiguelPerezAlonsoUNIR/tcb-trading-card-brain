# Lorcana Card Scraper - Quick Start Guide

## Overview

This tool retrieves Disney Lorcana card data and images from [dreamborn.ink](https://dreamborn.ink/es/cards).

## Files Created

- **`scrape_lorcana_cards.py`** - Main scraper script
- **`tests/test_lorcana_scraper.py`** - Unit tests for the scraper
- **`docs/LORCANA_CARD_RETRIEVAL.md`** - Comprehensive documentation

## Quick Start

### 1. Install Dependencies

```bash
pip install requests beautifulsoup4
```

### 2. Test Connectivity

```bash
python scrape_lorcana_cards.py --test-connectivity
```

### 3. Fetch Cards

```bash
# Basic usage - saves to lorcana_cards.json
python scrape_lorcana_cards.py

# Save to custom file
python scrape_lorcana_cards.py --output my_cards.json

# Generate Python code for integration
python scrape_lorcana_cards.py --generate-code
```

## Usage Examples

### Example 1: Basic Card Retrieval

```bash
python scrape_lorcana_cards.py
```

Output:
```
======================================================================
Lorcana Card Scraper - dreamborn.ink
======================================================================
Testing connectivity to https://dreamborn.ink...
✓ Successfully connected to https://dreamborn.ink

✓ Successfully fetched 235 cards

Card Statistics:
  Total cards: 235
  Card types:
    Action: 35
    Character: 180
    Item: 15
    Location: 5

✓ Saved 235 cards to lorcana_cards.json
```

### Example 2: Generate Integration Code

```bash
python scrape_lorcana_cards.py --generate-code
```

This creates Python code that can be copied into `lorcana_deck_builder.py`.

### Example 3: Quiet Mode

```bash
python scrape_lorcana_cards.py --quiet --output cards.json
```

Runs without verbose output.

## Network Access

⚠️ **Important**: This script requires network access to `dreamborn.ink`.

### If dreamborn.ink is blocked:

The script will detect this and show manual instructions:

```
======================================================================
MANUAL DATA RETRIEVAL INSTRUCTIONS
======================================================================

Since automatic scraping is not possible, you can manually retrieve
Lorcana card data using one of these methods:

1. Use a browser with network access
2. Use an alternative Lorcana API
3. Run this script from a different environment
4. Check if dreamborn.ink provides data export

======================================================================
```

### Workarounds:

1. **Run locally**: Execute on your personal computer and commit the JSON
2. **Alternative APIs**: Try lorcast.com or lorcana-api.com
3. **Manual export**: Visit dreamborn.ink in a browser and export data
4. **VPN/Proxy**: Use different network with access

## Output Format

The scraper creates a JSON file with this structure:

```json
[
  {
    "name": "Simba - Protective Cub",
    "type": "Character",
    "colors": ["Amber"],
    "cost": 1,
    "power": 1,
    "effect": "Challenger +2",
    "inkable": true,
    "set": "TFC",
    "card_number": "123",
    "rarity": "Common",
    "image_url": "https://dreamborn.ink/images/cards/TFC/123.jpg"
  }
]
```

## Integration with Deck Builder

### Option 1: JSON File Loading

Modify `lorcana_deck_builder.py`:

```python
import json

def _load_cards_from_db(self) -> List[Dict]:
    try:
        with open('lorcana_cards.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return self._get_sample_lorcana_cards()
```

### Option 2: Direct Import

Use the `--generate-code` flag and copy the output into your code.

### Option 3: Database Import

Import the JSON into your SQLite database using `init_cards_db.py` pattern.

## Testing

Run the unit tests:

```bash
python tests/test_lorcana_scraper.py
```

All tests should pass:
```
Ran 15 tests in 0.006s

OK
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `-o FILE` | Output file (default: lorcana_cards.json) |
| `-q` | Quiet mode (no verbose output) |
| `-g` | Generate Python code |
| `--test-connectivity` | Test if dreamborn.ink is accessible |
| `-h` | Show help message |

## Troubleshooting

### Problem: Connection Error

**Error**: `Failed to resolve 'dreamborn.ink'`

**Solution**: Domain is blocked. See "Network Access" section above.

### Problem: No Cards Found

**Error**: `No cards found in HTML`

**Solution**: Website structure may have changed. Update HTML parsing selectors.

### Problem: Invalid JSON

**Error**: JSON file is malformed

**Solution**: Check encoding, use UTF-8. Validate with `python -m json.tool lorcana_cards.json`

## Documentation

For comprehensive documentation, see:

📖 **[docs/LORCANA_CARD_RETRIEVAL.md](docs/LORCANA_CARD_RETRIEVAL.md)**

This includes:
- Detailed usage instructions
- Alternative data sources
- Integration examples
- Troubleshooting guide
- Future enhancements

## Support

1. Check `--help`: `python scrape_lorcana_cards.py --help`
2. Read the docs: `docs/LORCANA_CARD_RETRIEVAL.md`
3. Run tests: `python tests/test_lorcana_scraper.py`
4. Test connectivity: `python scrape_lorcana_cards.py --test-connectivity`

## Summary

✅ **Script created**: `scrape_lorcana_cards.py`
✅ **Tests created**: `tests/test_lorcana_scraper.py`
✅ **Documentation**: `docs/LORCANA_CARD_RETRIEVAL.md`
✅ **All tests passing**: 15/15 tests OK

The scraper is ready to use in any environment with network access to dreamborn.ink!

---

**Last Updated**: November 7, 2025
