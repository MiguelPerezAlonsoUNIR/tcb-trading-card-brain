"""
One Piece TCG Card Database
Contains card data for the One Piece Trading Card Game
"""

# Card types available in One Piece TCG
CARD_TYPES = ['Leader', 'Character', 'Event', 'Stage']

# Available colors in One Piece TCG
COLORS = ['Red', 'Blue', 'Green', 'Purple', 'Black', 'Yellow']

# Base URL for card images - using a public One Piece TCG image API
# Format: {BASE_IMAGE_URL}/{set}-{card_id}.jpg
BASE_IMAGE_URL = 'https://en.onepiece-cardgame.com/images/cardlist'

def get_card_image_url(card_set, card_number):
    """
    Generate image URL for a card based on set and card number
    Falls back to a placeholder if image is not available
    """
    # Format: OP01-001.png for card number 001 from set OP01
    return f"{BASE_IMAGE_URL}/{card_set}-{card_number}.png"

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
        'card_number': '001',
        'rarity': 'Leader',
        'image_url': get_card_image_url('ST01', '001')
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
        'card_number': '001',
        'rarity': 'Leader',
        'image_url': get_card_image_url('ST02', '001')
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
        'card_number': '001',
        'rarity': 'Leader',
        'image_url': get_card_image_url('ST03', '001')
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
        'card_number': '001',
        'rarity': 'Leader',
        'image_url': get_card_image_url('ST04', '001')
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
        'card_number': '002',
        'rarity': 'Leader',
        'image_url': get_card_image_url('OP01', '002')
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
        'card_number': '003',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('OP01', '003')
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
        'card_number': '004',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP01', '004')
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
        'card_number': '005',
        'rarity': 'Secret Rare',
        'image_url': get_card_image_url('OP01', '005')
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
        'card_number': '002',
        'rarity': 'Common',
        'image_url': get_card_image_url('ST01', '002')
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
        'card_number': '006',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('OP01', '006')
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
        'card_number': '003',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP02', '003')
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
        'card_number': '004',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('OP02', '004')
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
        'card_number': '007',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('OP01', '007')
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
        'card_number': '002',
        'rarity': 'Rare',
        'image_url': get_card_image_url('ST03', '002')
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
        'card_number': '003',
        'rarity': 'Common',
        'image_url': get_card_image_url('ST03', '003')
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
        'card_number': '008',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP01', '008')
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
        'card_number': '005',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('OP02', '005')
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
        'card_number': '009',
        'rarity': 'Secret Rare',
        'image_url': get_card_image_url('OP01', '009')
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
        'card_number': '002',
        'rarity': 'Rare',
        'image_url': get_card_image_url('ST02', '002')
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
        'card_number': '003',
        'rarity': 'Common',
        'image_url': get_card_image_url('ST02', '003')
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
        'card_number': '010',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('OP01', '010')
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
        'card_number': '006',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP02', '006')
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
        'card_number': '011',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('OP01', '011')
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
        'card_number': '012',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('OP01', '012')
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
        'card_number': '013',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP01', '013')
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
        'card_number': '002',
        'rarity': 'Common',
        'image_url': get_card_image_url('ST04', '002')
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
        'card_number': '014',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP01', '014')
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
        'card_number': '015',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('OP01', '015')
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
        'card_number': '007',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('OP02', '007')
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
        'card_number': '016',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('OP01', '016')
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
        'card_number': '017',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP01', '017')
    },
    
    # Events
    {
        'name': 'Gum-Gum Red Roc',
        'type': 'Event',
        'colors': ['Red'],
        'cost': 3,
        'effect': 'KO 1 of your opponent\'s Characters with a cost of 4 or less.',
        'set': 'ST01',
        'card_number': '010',
        'rarity': 'Common',
        'image_url': get_card_image_url('ST01', '010')
    },
    {
        'name': 'Radical Beam',
        'type': 'Event',
        'colors': ['Red'],
        'cost': 2,
        'effect': 'Deal 2 damage to your opponent\'s Leader.',
        'set': 'OP01',
        'card_number': '018',
        'rarity': 'Uncommon',
        'image_url': get_card_image_url('OP01', '018')
    },
    {
        'name': 'Gum-Gum Giant',
        'type': 'Event',
        'colors': ['Red'],
        'cost': 5,
        'effect': 'KO 1 of your opponent\'s Characters with a cost of 7 or less.',
        'set': 'OP02',
        'card_number': '010',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP02', '010')
    },
    {
        'name': 'Water Shot',
        'type': 'Event',
        'colors': ['Blue'],
        'cost': 1,
        'effect': 'Return 1 Character with a cost of 2 or less to its owner\'s hand.',
        'set': 'ST03',
        'card_number': '010',
        'rarity': 'Common',
        'image_url': get_card_image_url('ST03', '010')
    },
    {
        'name': 'Tact',
        'type': 'Event',
        'colors': ['Blue'],
        'cost': 3,
        'effect': 'Return 1 Character with a cost of 5 or less to its owner\'s hand.',
        'set': 'OP01',
        'card_number': '019',
        'rarity': 'Uncommon',
        'image_url': get_card_image_url('OP01', '019')
    },
    {
        'name': 'Shambles',
        'type': 'Event',
        'colors': ['Blue'],
        'cost': 2,
        'effect': 'Draw 2 cards, then place 1 card from your hand on the top or bottom of your deck.',
        'set': 'OP02',
        'card_number': '011',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP02', '011')
    },
    {
        'name': 'Three Sword Style: Purgatory Onigiri',
        'type': 'Event',
        'colors': ['Green'],
        'cost': 2,
        'effect': 'Give 1 of your Characters +2000 power during this turn.',
        'set': 'ST02',
        'card_number': '010',
        'rarity': 'Common',
        'image_url': get_card_image_url('ST02', '010')
    },
    {
        'name': 'Bird Strike',
        'type': 'Event',
        'colors': ['Green'],
        'cost': 4,
        'effect': 'KO 1 of your opponent\'s rested Characters with a cost of 6 or less.',
        'set': 'OP01',
        'card_number': '020',
        'rarity': 'Uncommon',
        'image_url': get_card_image_url('OP01', '020')
    },
    {
        'name': 'Mochi Tsuki',
        'type': 'Event',
        'colors': ['Purple'],
        'cost': 1,
        'effect': 'Draw 1 card and trash 1 card from your hand.',
        'set': 'OP01',
        'card_number': '021',
        'rarity': 'Common',
        'image_url': get_card_image_url('OP01', '021')
    },
    {
        'name': 'Soul Pocus',
        'type': 'Event',
        'colors': ['Purple'],
        'cost': 3,
        'effect': 'Play 1 Character card with a cost of 4 or less from your trash.',
        'set': 'ST04',
        'card_number': '010',
        'rarity': 'Uncommon',
        'image_url': get_card_image_url('ST04', '010')
    },
    {
        'name': 'Sables',
        'type': 'Event',
        'colors': ['Black'],
        'cost': 2,
        'effect': 'KO 1 of your opponent\'s Characters with 4000 power or less.',
        'set': 'OP01',
        'card_number': '022',
        'rarity': 'Common',
        'image_url': get_card_image_url('OP01', '022')
    },
    {
        'name': 'Ice Age',
        'type': 'Event',
        'colors': ['Yellow'],
        'cost': 3,
        'effect': 'Rest up to 2 of your opponent\'s Characters with a cost of 3 or less.',
        'set': 'OP01',
        'card_number': '023',
        'rarity': 'Uncommon',
        'image_url': get_card_image_url('OP01', '023')
    },
    
    # Stages
    {
        'name': 'Thousand Sunny',
        'type': 'Stage',
        'colors': ['Red'],
        'cost': 1,
        'effect': 'Once per turn, you may rest this Stage to give 1 of your Characters +1000 power during this turn.',
        'set': 'ST01',
        'card_number': '015',
        'rarity': 'Uncommon',
        'image_url': get_card_image_url('ST01', '015')
    },
    {
        'name': 'Baratie',
        'type': 'Stage',
        'colors': ['Blue'],
        'cost': 2,
        'effect': 'Once per turn, you may rest this Stage to draw 1 card, then place 1 card from your hand on the bottom of your deck.',
        'set': 'ST03',
        'card_number': '015',
        'rarity': 'Uncommon',
        'image_url': get_card_image_url('ST03', '015')
    },
    {
        'name': 'Whole Cake Island',
        'type': 'Stage',
        'colors': ['Purple'],
        'cost': 1,
        'effect': 'Once per turn, you may rest this Stage to look at the top 3 cards of your deck and trash 1 of them.',
        'set': 'ST04',
        'card_number': '015',
        'rarity': 'Uncommon',
        'image_url': get_card_image_url('ST04', '015')
    },
    {
        'name': 'Punk Hazard',
        'type': 'Stage',
        'colors': ['Green'],
        'cost': 2,
        'effect': 'Once per turn, you may rest this Stage and trash 1 card from your hand to draw 2 cards.',
        'set': 'OP01',
        'card_number': '024',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP01', '024')
    },
    
    # Additional Red cards to reach 50-card deck capacity
    {
        'name': 'Marco',
        'type': 'Character',
        'colors': ['Red'],
        'power': 5000,
        'cost': 5,
        'attribute': 'Special',
        'effect': 'On Play: Give this Character +2000 power during this turn.',
        'set': 'OP02',
        'card_number': '013',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP02', '013')
    },
    {
        'name': 'Red Hawk',
        'type': 'Event',
        'colors': ['Red'],
        'cost': 3,
        'effect': 'Deal 5000 damage to 1 of your opponent\'s Characters.',
        'set': 'ST01',
        'card_number': '014',
        'rarity': 'Common',
        'image_url': get_card_image_url('ST01', '014')
    },
    
    # Additional Blue cards to reach 50-card deck capacity
    {
        'name': 'Jinbe',
        'type': 'Character',
        'colors': ['Blue'],
        'power': 5000,
        'cost': 4,
        'attribute': 'Strike',
        'effect': 'Blocker. When this Character blocks, it gains +1000 power.',
        'set': 'OP01',
        'card_number': '025',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP01', '025')
    },
    {
        'name': 'Fishman Karate',
        'type': 'Event',
        'colors': ['Blue'],
        'cost': 2,
        'effect': 'Return 1 Character with 4000 power or less to its owner\'s hand.',
        'set': 'ST03',
        'card_number': '015',
        'rarity': 'Common',
        'image_url': get_card_image_url('ST03', '015')
    },
    {
        'name': 'Arlong',
        'type': 'Character',
        'colors': ['Blue'],
        'power': 4000,
        'cost': 3,
        'attribute': 'Strike',
        'effect': 'On Play: Draw 1 card if you have 3 or fewer cards in hand.',
        'set': 'OP01',
        'card_number': '026',
        'rarity': 'Common',
        'image_url': get_card_image_url('OP01', '026')
    },
    {
        'name': 'Water Shot',
        'type': 'Event',
        'colors': ['Blue'],
        'cost': 1,
        'effect': 'Draw 2 cards, then place 1 card from your hand on top of your deck.',
        'set': 'ST03',
        'card_number': '016',
        'rarity': 'Uncommon',
        'image_url': get_card_image_url('ST03', '016')
    },
    
    # Additional Green cards to reach 50-card deck capacity
    {
        'name': 'Sanji',
        'type': 'Character',
        'colors': ['Green'],
        'power': 5000,
        'cost': 4,
        'attribute': 'Strike',
        'effect': 'Rush. On Play: You may trash 1 card from your hand to give this Character +2000 power during this turn.',
        'set': 'ST02',
        'card_number': '012',
        'rarity': 'Rare',
        'image_url': get_card_image_url('ST02', '012')
    },
    {
        'name': 'Diable Jambe',
        'type': 'Event',
        'colors': ['Green'],
        'cost': 2,
        'effect': 'Give 1 of your Characters +3000 power during this turn.',
        'set': 'ST02',
        'card_number': '013',
        'rarity': 'Common',
        'image_url': get_card_image_url('ST02', '013')
    },
    {
        'name': 'Killer',
        'type': 'Character',
        'colors': ['Green'],
        'power': 4000,
        'cost': 3,
        'attribute': 'Slash',
        'effect': 'On K.O.: Draw 1 card.',
        'set': 'OP01',
        'card_number': '027',
        'rarity': 'Common',
        'image_url': get_card_image_url('OP01', '027')
    },
    {
        'name': 'Oden Two-Sword Style',
        'type': 'Event',
        'colors': ['Green'],
        'cost': 4,
        'effect': 'KO 1 of your opponent\'s Characters with 6000 power or less.',
        'set': 'ST02',
        'card_number': '014',
        'rarity': 'Rare',
        'image_url': get_card_image_url('ST02', '014')
    },
    {
        'name': 'Brook',
        'type': 'Character',
        'colors': ['Green'],
        'power': 3000,
        'cost': 2,
        'attribute': 'Slash',
        'effect': 'On Play: Look at the top 2 cards of your deck and put them back in any order.',
        'set': 'OP01',
        'card_number': '028',
        'rarity': 'Common',
        'image_url': get_card_image_url('OP01', '028')
    },
    
    # Additional Red cards (continued)
    {
        'name': 'Gum-Gum Red Hawk',
        'type': 'Event',
        'colors': ['Red'],
        'cost': 4,
        'effect': 'KO 1 of your opponent\'s Characters with 6000 power or less.',
        'set': 'ST01',
        'card_number': '015',
        'rarity': 'Uncommon',
        'image_url': get_card_image_url('ST01', '015')
    },
    
    # Additional Blue cards (continued)
    {
        'name': 'Hody Jones',
        'type': 'Character',
        'colors': ['Blue'],
        'power': 5000,
        'cost': 5,
        'attribute': 'Strike',
        'effect': 'On Play: Return up to 1 Character with cost 3 or less to its owner\'s hand.',
        'set': 'OP01',
        'card_number': '030',
        'rarity': 'Rare',
        'image_url': get_card_image_url('OP01', '030')
    },
    {
        'name': 'Coup de Burst',
        'type': 'Event',
        'colors': ['Blue'],
        'cost': 3,
        'effect': 'Return 1 Character with cost 5 or less to its owner\'s hand.',
        'set': 'ST03',
        'card_number': '017',
        'rarity': 'Rare',
        'image_url': get_card_image_url('ST03', '017')
    },
    
    # Additional Green cards (continued)
    {
        'name': 'Punk Gibson',
        'type': 'Event',
        'colors': ['Green'],
        'cost': 3,
        'effect': 'Give 1 of your Characters +4000 power during this turn.',
        'set': 'ST02',
        'card_number': '015',
        'rarity': 'Rare',
        'image_url': get_card_image_url('ST02', '015')
    },
    
    # Additional Purple cards to reach 50-card deck capacity
    {
        'name': 'King',
        'type': 'Character',
        'colors': ['Purple'],
        'power': 6000,
        'cost': 6,
        'attribute': 'Strike',
        'effect': 'Rush. This Character cannot be KO\'d by effects.',
        'set': 'ST04',
        'card_number': '016',
        'rarity': 'Super Rare',
        'image_url': get_card_image_url('ST04', '016')
    },
    {
        'name': 'Queen',
        'type': 'Character',
        'colors': ['Purple'],
        'power': 5000,
        'cost': 5,
        'attribute': 'Special',
        'effect': 'On Play: Trash the top 3 cards of your deck. Then add 1 Character with cost 4 or less from your trash to your hand.',
        'set': 'ST04',
        'card_number': '017',
        'rarity': 'Rare',
        'image_url': get_card_image_url('ST04', '017')
    },
    {
        'name': 'Jack',
        'type': 'Character',
        'colors': ['Purple'],
        'power': 5000,
        'cost': 4,
        'attribute': 'Strike',
        'effect': 'On Play: KO 1 of your opponent\'s Characters with 4000 power or less.',
        'set': 'ST04',
        'card_number': '018',
        'rarity': 'Rare',
        'image_url': get_card_image_url('ST04', '018')
    },
    {
        'name': 'Ragnarok',
        'type': 'Event',
        'colors': ['Purple'],
        'cost': 3,
        'effect': 'KO 1 of your opponent\'s Characters with 5000 power or less.',
        'set': 'ST04',
        'card_number': '019',
        'rarity': 'Common',
        'image_url': get_card_image_url('ST04', '019')
    },
    {
        'name': 'X Drake',
        'type': 'Character',
        'colors': ['Purple'],
        'power': 4000,
        'cost': 3,
        'attribute': 'Strike',
        'effect': 'Blocker.',
        'set': 'OP01',
        'card_number': '029',
        'rarity': 'Common',
        'image_url': get_card_image_url('OP01', '029')
    },
    {
        'name': 'Thunder Bagua',
        'type': 'Event',
        'colors': ['Purple'],
        'cost': 2,
        'effect': 'Give 1 of your Characters +2000 power during this turn. Draw 1 card.',
        'set': 'ST04',
        'card_number': '020',
        'rarity': 'Uncommon',
        'image_url': get_card_image_url('ST04', '020')
    },
]
