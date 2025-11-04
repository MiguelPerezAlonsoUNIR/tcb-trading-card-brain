# One Piece TCG Rules Implementation

This document describes how the One Piece Trading Card Game official rules are implemented in this deck builder application.

## Rule Source

The official One Piece TCG rules can be found at:
https://en.onepiece-cardgame.com/pdf/rule_manual.pdf

## Implemented Rules

### 1. Color Matching Rule

**Rule**: Cards in a deck can only be from the same color(s) as the leader.

**Implementation**: 
- Located in `deck_builder.py`, method `_build_main_deck()`
- Filters available cards to only include those that share at least one color with the leader
- The filter uses: `any(lc in c['colors'] for lc in leader['colors'])`
- This works for both single-color and multi-color leaders

**Examples**:
- **Single Color**: Monkey D. Luffy (Red) → Only Red cards allowed
- **Multi Color**: Trafalgar Law (Blue/Black) → Blue cards, Black cards, or Blue/Black cards allowed

### 2. Maximum Card Copies Rule

**Rule**: Maximum 4 copies of any single card (excluding Leaders).

**Implementation**:
- Located in `deck_builder.py`, class variable `max_copies = 4`
- Enforced in `_build_main_deck()` method with condition: `if self._count_card_copies(main_deck, card) < self.max_copies`
- Helper method `_count_card_copies()` counts instances of a card by name

### 3. Deck Size Rule

**Rule**: Main deck must contain exactly 50 cards (excluding the Leader).

**Implementation**:
- Located in `deck_builder.py`, class variable `deck_size = 50`
- Target enforced in `_build_main_deck()` method: `while len(main_deck) < self.deck_size`
- Deck analyzer warns if deck size is not exactly 50 cards

**Note**: Due to limited card database, some color combinations may not reach 50 cards while respecting the color matching rule.

### 4. One Leader Per Deck Rule

**Rule**: Each deck must have exactly 1 Leader card.

**Implementation**:
- Leaders are selected separately in `_select_leader()` method
- Leaders are excluded from main deck filtering: `if c['type'] != 'Leader'`
- Deck structure includes a dedicated `leader` field

## Testing

Color rule enforcement is tested in `test_color_rules.py`:

1. **Single Color Leader Test**: Verifies single-color leaders only get matching cards
2. **Multi-Color Leader Test**: Verifies multi-color leaders accept cards from any of their colors
3. **'Any' Color Parameter Test**: Verifies the 'any' parameter still enforces leader color matching
4. **Color Distribution Test**: Analyzes and validates color distribution across different decks

Run the tests:
```bash
python test_color_rules.py
```

## Code Changes

### Modified Files

1. **deck_builder.py**
   - Removed fallback that allowed non-matching colors when card pool was exhausted
   - Updated color filtering to always respect leader colors regardless of `color` parameter
   - Simplified logic by removing the `color == 'any'` bypass

### Added Files

1. **test_color_rules.py**
   - Comprehensive test suite for color rule enforcement
   - Tests single-color, multi-color, and parameter combinations
   - Validates color distribution in generated decks

2. **ONE_PIECE_TCG_RULES.md** (this file)
   - Documentation of rule implementation
   - Reference guide for developers

### Documentation Updates

1. **README.md**
   - Added "One Piece TCG Rules Compliance" section
   - Updated deck building instructions with rule notes
   - Added note about database limitations

## Card Database Limitations

Currently, the card database (`cards_data.py`) contains:
- Red: 11 unique cards (44 maximum with 4x copies)
- Blue: 9 unique cards (36 maximum with 4x copies)
- Green: 8 unique cards (32 maximum with 4x copies)
- Purple: 7 unique cards (28 maximum with 4x copies)
- Black: 4 unique cards (16 maximum with 4x copies)
- Yellow: 3 unique cards (12 maximum with 4x copies)

To build full 50-card decks for all colors, more cards need to be added to the database. Multi-color leaders (like Trafalgar Law with Blue/Black) can combine card pools to reach 50 cards.

## Combat Rules Implementation

### 5. Combat Simulation Rules

**Rules**: The combat simulator follows official One Piece TCG game mechanics.

**Implementation**:
- Located in `combat_simulator.py`, method `simulate_game_with_rules()`
- Implements actual One Piece TCG turn structure and combat resolution
- Key mechanics:
  - **DON!! System**: Players gain DON!! cards each turn (up to 10) to pay for characters
  - **Life System**: Leaders have life points, game ends when reduced to 0
  - **Power-based Combat**: Characters battle based on power values, higher power wins
  - **Blocker Mechanic**: Characters with Blocker ability must be attacked before leader
  - **Leader Abilities**: Effects like "+1000 power during your turn" are applied
  - **Character Effects**: "When attacking" effects modify power during combat

**Combat Flow**:
1. **DON!! Phase**: Active player gains DON!! equal to turn number (max 10)
2. **Draw Phase**: Active player draws 1 card
3. **Main Phase**: Player can play Character cards by paying their DON!! cost
4. **Attack Phase**: 
   - Characters can attack opponent's leader or characters
   - Blockers must be dealt with before attacking leader
   - Power comparison determines battle outcome
   - Successful leader attacks deal 1 life damage

**Examples**:
- Character with 5000 power attacks blocker with 4000 power → Blocker is KO'd
- Character with 4000 power attacks 5000 power character → Attacker is KO'd
- Character with 5000 power attacks leader with no blockers → Leader takes 1 damage
- Monkey D. Luffy's effect: Characters gain +1000 power during your turn

## Future Enhancements

Potential improvements to rules enforcement:

1. **Counter System**: Implement counter card values for defensive plays
2. **DON!! Attachments**: Allow attaching DON!! to characters to boost power
3. **Event Card Effects**: Full implementation of event card timing and effects
4. **Stage Cards**: Persistent effects from stage cards
5. **Rush Keyword**: Characters with Rush can attack immediately when played
6. **Card Attributes**: Enforce attribute-based rules if any exist
7. **Set Restrictions**: Implement tournament format restrictions (Standard, etc.)
8. **Ban List**: Support for banned/restricted card lists
9. **Enhanced Validation**: More comprehensive deck validation before saving

## References

- [One Piece Card Game Official Website](https://en.onepiece-cardgame.com/)
- [One Piece TCG Rule Manual PDF](https://en.onepiece-cardgame.com/pdf/rule_manual.pdf)
