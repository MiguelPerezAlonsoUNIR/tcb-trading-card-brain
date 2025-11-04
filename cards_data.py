"""
One Piece TCG Card Database
Contains card data for the One Piece Trading Card Game
"""

# Card types available in One Piece TCG
CARD_TYPES = ['Leader', 'Character', 'Event', 'Stage']

# Available colors in One Piece TCG
COLORS = ['Red', 'Blue', 'Green', 'Purple', 'Black', 'Yellow']

# Sample One Piece TCG cards database
ONEPIECE_CARDS = [
    # Leaders
    {
        'name': 'Monkey D. Luffy',
        'type': 'Leader',
        'colors': ['Red'],
        'power': 5000,
        'life': 5,
        'attribute': 'Strike',
        'cost': 0,
        'effect': 'Your Characters gain +1000 power during your turn.',
        'set': 'ST01',
        'rarity': 'Leader'
    },
    {
        'name': 'Roronoa Zoro',
        'type': 'Leader',
        'colors': ['Green'],
        'power': 5000,
        'life': 5,
        'attribute': 'Slash',
        'cost': 0,
        'effect': 'When attacking, you may trash 1 card from your hand to give this Leader +1000 power during this battle.',
        'set': 'ST02',
        'rarity': 'Leader'
    },
    {
        'name': 'Nami',
        'type': 'Leader',
        'colors': ['Blue'],
        'power': 5000,
        'life': 4,
        'attribute': 'Special',
        'cost': 0,
        'effect': 'Once per turn, you may return 1 of your Characters to your hand to draw 1 card.',
        'set': 'ST03',
        'rarity': 'Leader'
    },
    {
        'name': 'Kaido',
        'type': 'Leader',
        'colors': ['Purple'],
        'power': 6000,
        'life': 5,
        'attribute': 'Strike',
        'cost': 0,
        'effect': 'Once per turn, you may trash 1 card from your hand to give all your Characters +1000 power during this turn.',
        'set': 'ST04',
        'rarity': 'Leader'
    },
    {
        'name': 'Trafalgar Law',
        'type': 'Leader',
        'colors': ['Blue', 'Black'],
        'power': 5000,
        'life': 4,
        'attribute': 'Slash',
        'cost': 0,
        'effect': 'Once per turn, you may pay 2 to play 1 Character card with a cost of 3 or less from your hand.',
        'set': 'OP01',
        'rarity': 'Leader'
    },
    
    # Red Characters
    {
        'name': 'Portgas D. Ace',
        'type': 'Character',
        'colors': ['Red'],
        'power': 6000,
        'cost': 5,
        'attribute': 'Special',
        'effect': 'On Play: KO 1 of your opponent\'s Characters with a cost of 3 or less.',
        'set': 'OP01',
        'rarity': 'Super Rare'
    },
    {
        'name': 'Sabo',
        'type': 'Character',
        'colors': ['Red'],
        'power': 5000,
        'cost': 4,
        'attribute': 'Special',
        'effect': 'On Play: Draw 1 card if you have 3 or fewer cards in your hand.',
        'set': 'OP01',
        'rarity': 'Rare'
    },
    {
        'name': 'Shanks',
        'type': 'Character',
        'colors': ['Red'],
        'power': 9000,
        'cost': 9,
        'attribute': 'Slash',
        'effect': 'Rush. On Play: Return all Characters with a cost of 5 or less to their owner\'s hands.',
        'set': 'OP01',
        'rarity': 'Secret Rare'
    },
    {
        'name': 'Koby',
        'type': 'Character',
        'colors': ['Red'],
        'power': 2000,
        'cost': 1,
        'attribute': 'Strike',
        'effect': 'Blocker.',
        'set': 'ST01',
        'rarity': 'Common'
    },
    {
        'name': 'Eustass Kid',
        'type': 'Character',
        'colors': ['Red'],
        'power': 7000,
        'cost': 7,
        'attribute': 'Strike',
        'effect': 'On Play: Deal 1 damage to your opponent\'s Leader.',
        'set': 'OP01',
        'rarity': 'Super Rare'
    },
    {
        'name': 'Uta',
        'type': 'Character',
        'colors': ['Red'],
        'power': 4000,
        'cost': 3,
        'attribute': 'Special',
        'effect': 'When attacking, this Character gains +2000 power.',
        'set': 'OP02',
        'rarity': 'Rare'
    },
    {
        'name': 'Garp',
        'type': 'Character',
        'colors': ['Red'],
        'power': 6000,
        'cost': 5,
        'attribute': 'Strike',
        'effect': 'Blocker. On Play: Draw 1 card and trash 1 card from your hand.',
        'set': 'OP02',
        'rarity': 'Super Rare'
    },
    
    # Blue Characters
    {
        'name': 'Donquixote Doflamingo',
        'type': 'Character',
        'colors': ['Blue'],
        'power': 6000,
        'cost': 5,
        'attribute': 'Special',
        'effect': 'On Play: Return 1 Character with a cost of 4 or less to its owner\'s hand.',
        'set': 'OP01',
        'rarity': 'Super Rare'
    },
    {
        'name': 'Nico Robin',
        'type': 'Character',
        'colors': ['Blue'],
        'power': 4000,
        'cost': 3,
        'attribute': 'Special',
        'effect': 'On Play: Look at the top 3 cards of your deck and rearrange them in any order.',
        'set': 'ST03',
        'rarity': 'Rare'
    },
    {
        'name': 'Tony Tony Chopper',
        'type': 'Character',
        'colors': ['Blue'],
        'power': 3000,
        'cost': 2,
        'attribute': 'Wisdom',
        'effect': 'On Play: Draw 1 card if you have 3 or fewer cards in your hand.',
        'set': 'ST03',
        'rarity': 'Common'
    },
    {
        'name': 'Jinbe',
        'type': 'Character',
        'colors': ['Blue'],
        'power': 5000,
        'cost': 4,
        'attribute': 'Strike',
        'effect': 'Blocker. This Character cannot be KO\'d in battle by an opposing Character with 6000 power or less.',
        'set': 'OP01',
        'rarity': 'Rare'
    },
    {
        'name': 'Marco',
        'type': 'Character',
        'colors': ['Blue'],
        'power': 5000,
        'cost': 5,
        'attribute': 'Special',
        'effect': 'On K.O.: Play this card from your trash rested.',
        'set': 'OP02',
        'rarity': 'Super Rare'
    },
    
    # Green Characters
    {
        'name': 'Dracule Mihawk',
        'type': 'Character',
        'colors': ['Green'],
        'power': 9000,
        'cost': 9,
        'attribute': 'Slash',
        'effect': 'Rush. When attacking, you may trash 1 card from your hand to give this Character +2000 power.',
        'set': 'OP01',
        'rarity': 'Secret Rare'
    },
    {
        'name': 'Sanji',
        'type': 'Character',
        'colors': ['Green'],
        'power': 5000,
        'cost': 4,
        'attribute': 'Strike',
        'effect': 'On Play: If your Leader is Zoro, this Character gains +2000 power during this turn.',
        'set': 'ST02',
        'rarity': 'Rare'
    },
    {
        'name': 'Usopp',
        'type': 'Character',
        'colors': ['Green'],
        'power': 3000,
        'cost': 2,
        'attribute': 'Ranged',
        'effect': 'On Play: You may trash 1 card from your hand to draw 2 cards.',
        'set': 'ST02',
        'rarity': 'Common'
    },
    {
        'name': 'Oden Kozuki',
        'type': 'Character',
        'colors': ['Green'],
        'power': 6000,
        'cost': 6,
        'attribute': 'Slash',
        'effect': 'Rush. Double Attack.',
        'set': 'OP01',
        'rarity': 'Super Rare'
    },
    {
        'name': 'Yamato',
        'type': 'Character',
        'colors': ['Green'],
        'power': 5000,
        'cost': 5,
        'attribute': 'Strike',
        'effect': 'Rush. On Play: Trash the top 3 cards of your deck.',
        'set': 'OP02',
        'rarity': 'Rare'
    },
    
    # Purple Characters
    {
        'name': 'Charlotte Katakuri',
        'type': 'Character',
        'colors': ['Purple'],
        'power': 7000,
        'cost': 6,
        'attribute': 'Special',
        'effect': 'On Play: Draw 1 card and trash 1 card from your hand.',
        'set': 'OP01',
        'rarity': 'Super Rare'
    },
    {
        'name': 'Big Mom',
        'type': 'Character',
        'colors': ['Purple'],
        'power': 8000,
        'cost': 8,
        'attribute': 'Strike',
        'effect': 'On Play: Trash the top 3 cards of your deck, then play 1 Character with a cost of 5 or less from your trash.',
        'set': 'OP01',
        'rarity': 'Super Rare'
    },
    {
        'name': 'Perospero',
        'type': 'Character',
        'colors': ['Purple'],
        'power': 4000,
        'cost': 3,
        'attribute': 'Special',
        'effect': 'On Play: Look at the top 3 cards of your deck and place them back in any order.',
        'set': 'OP01',
        'rarity': 'Rare'
    },
    {
        'name': 'Smoothie',
        'type': 'Character',
        'colors': ['Purple'],
        'power': 5000,
        'cost': 4,
        'attribute': 'Slash',
        'effect': 'Blocker.',
        'set': 'ST04',
        'rarity': 'Common'
    },
    
    # Black Characters
    {
        'name': 'Crocodile',
        'type': 'Character',
        'colors': ['Black'],
        'power': 5000,
        'cost': 5,
        'attribute': 'Special',
        'effect': 'On Play: KO 1 of your opponent\'s Characters with 3000 power or less.',
        'set': 'OP01',
        'rarity': 'Rare'
    },
    {
        'name': 'Rob Lucci',
        'type': 'Character',
        'colors': ['Black'],
        'power': 6000,
        'cost': 5,
        'attribute': 'Strike',
        'effect': 'Rush. On K.O.: Draw 1 card.',
        'set': 'OP01',
        'rarity': 'Super Rare'
    },
    {
        'name': 'Bartholomew Kuma',
        'type': 'Character',
        'colors': ['Black'],
        'power': 7000,
        'cost': 7,
        'attribute': 'Strike',
        'effect': 'On Play: Return 1 Character to its owner\'s hand.',
        'set': 'OP02',
        'rarity': 'Super Rare'
    },
    
    # Yellow Characters
    {
        'name': 'Borsalino',
        'type': 'Character',
        'colors': ['Yellow'],
        'power': 6000,
        'cost': 6,
        'attribute': 'Ranged',
        'effect': 'Blocker. On Play: KO 1 of your opponent\'s rested Characters with a cost of 4 or less.',
        'set': 'OP01',
        'rarity': 'Super Rare'
    },
    {
        'name': 'Issho',
        'type': 'Character',
        'colors': ['Yellow'],
        'power': 5000,
        'cost': 5,
        'attribute': 'Slash',
        'effect': 'On Play: Rest 1 of your opponent\'s Characters with a cost of 5 or less.',
        'set': 'OP01',
        'rarity': 'Rare'
    },
    
    # Events
    {
        'name': 'Gum-Gum Red Roc',
        'type': 'Event',
        'colors': ['Red'],
        'cost': 3,
        'effect': 'KO 1 of your opponent\'s Characters with a cost of 4 or less.',
        'set': 'ST01',
        'rarity': 'Common'
    },
    {
        'name': 'Radical Beam',
        'type': 'Event',
        'colors': ['Red'],
        'cost': 2,
        'effect': 'Deal 2 damage to your opponent\'s Leader.',
        'set': 'OP01',
        'rarity': 'Uncommon'
    },
    {
        'name': 'Gum-Gum Giant',
        'type': 'Event',
        'colors': ['Red'],
        'cost': 5,
        'effect': 'KO 1 of your opponent\'s Characters with a cost of 7 or less.',
        'set': 'OP02',
        'rarity': 'Rare'
    },
    {
        'name': 'Water Shot',
        'type': 'Event',
        'colors': ['Blue'],
        'cost': 1,
        'effect': 'Return 1 Character with a cost of 2 or less to its owner\'s hand.',
        'set': 'ST03',
        'rarity': 'Common'
    },
    {
        'name': 'Tact',
        'type': 'Event',
        'colors': ['Blue'],
        'cost': 3,
        'effect': 'Return 1 Character with a cost of 5 or less to its owner\'s hand.',
        'set': 'OP01',
        'rarity': 'Uncommon'
    },
    {
        'name': 'Shambles',
        'type': 'Event',
        'colors': ['Blue'],
        'cost': 2,
        'effect': 'Draw 2 cards, then place 1 card from your hand on the top or bottom of your deck.',
        'set': 'OP02',
        'rarity': 'Rare'
    },
    {
        'name': 'Three Sword Style: Purgatory Onigiri',
        'type': 'Event',
        'colors': ['Green'],
        'cost': 2,
        'effect': 'Give 1 of your Characters +2000 power during this turn.',
        'set': 'ST02',
        'rarity': 'Common'
    },
    {
        'name': 'Bird Strike',
        'type': 'Event',
        'colors': ['Green'],
        'cost': 4,
        'effect': 'KO 1 of your opponent\'s rested Characters with a cost of 6 or less.',
        'set': 'OP01',
        'rarity': 'Uncommon'
    },
    {
        'name': 'Mochi Tsuki',
        'type': 'Event',
        'colors': ['Purple'],
        'cost': 1,
        'effect': 'Draw 1 card and trash 1 card from your hand.',
        'set': 'OP01',
        'rarity': 'Common'
    },
    {
        'name': 'Soul Pocus',
        'type': 'Event',
        'colors': ['Purple'],
        'cost': 3,
        'effect': 'Play 1 Character card with a cost of 4 or less from your trash.',
        'set': 'ST04',
        'rarity': 'Uncommon'
    },
    {
        'name': 'Sables',
        'type': 'Event',
        'colors': ['Black'],
        'cost': 2,
        'effect': 'KO 1 of your opponent\'s Characters with 4000 power or less.',
        'set': 'OP01',
        'rarity': 'Common'
    },
    {
        'name': 'Ice Age',
        'type': 'Event',
        'colors': ['Yellow'],
        'cost': 3,
        'effect': 'Rest up to 2 of your opponent\'s Characters with a cost of 3 or less.',
        'set': 'OP01',
        'rarity': 'Uncommon'
    },
    
    # Stages
    {
        'name': 'Thousand Sunny',
        'type': 'Stage',
        'colors': ['Red'],
        'cost': 1,
        'effect': 'Once per turn, you may rest this Stage to give 1 of your Characters +1000 power during this turn.',
        'set': 'ST01',
        'rarity': 'Uncommon'
    },
    {
        'name': 'Baratie',
        'type': 'Stage',
        'colors': ['Blue'],
        'cost': 2,
        'effect': 'Once per turn, you may rest this Stage to draw 1 card, then place 1 card from your hand on the bottom of your deck.',
        'set': 'ST03',
        'rarity': 'Uncommon'
    },
    {
        'name': 'Whole Cake Island',
        'type': 'Stage',
        'colors': ['Purple'],
        'cost': 1,
        'effect': 'Once per turn, you may rest this Stage to look at the top 3 cards of your deck and trash 1 of them.',
        'set': 'ST04',
        'rarity': 'Uncommon'
    },
    {
        'name': 'Punk Hazard',
        'type': 'Stage',
        'colors': ['Green'],
        'cost': 2,
        'effect': 'Once per turn, you may rest this Stage and trash 1 card from your hand to draw 2 cards.',
        'set': 'OP01',
        'rarity': 'Rare'
    },
]
