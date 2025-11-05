"""
Structure Deck definitions for One Piece TCG
Contains deck lists for ST-01 through ST-28 starter/structure decks
"""

# Structure deck definitions
# Each deck contains a deck code, name, description, and list of cards with quantities
STRUCTURE_DECKS = {
    'ST-01': {
        'code': 'ST-01',
        'name': 'Straw Hat Crew [Red]',
        'description': 'A red-themed deck centered around Monkey D. Luffy and the Straw Hat crew',
        'color': 'Red',
        'leader': 'Monkey D. Luffy',
        'cards': {
            'Monkey D. Luffy': 1,  # Leader
            'Portgas D. Ace': 4,
            'Tony Tony Chopper': 4,
            'Sanji': 4,
            'Roronoa Zoro': 4,
            'Gum-Gum Red Roc': 4,
            'Gum-Gum Jet Pistol': 4,
            'Fire Fist': 4,
            'Thriller Bark': 2,
            'Going Merry': 2,
            # Fill remaining slots with common red cards
            'Nico Robin': 4,
            'Usopp': 4,
            'Diable Jambe': 3,
            'Radical Beam': 4,
            'Thousand Sunny': 2,
        }
    },
    'ST-02': {
        'code': 'ST-02',
        'name': 'Worst Generation [Green]',
        'description': 'A green-themed deck featuring Eustass Kid and the Worst Generation',
        'color': 'Green',
        'leader': 'Eustass Kid',
        'cards': {
            'Eustass Kid': 1,  # Leader
            'Roronoa Zoro': 4,
            'Trafalgar Law': 4,
            'Killer': 4,
            'X Drake': 4,
            'Onigiri': 4,
            'Punk Rotten': 4,
            'Shambles': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            # Fill remaining slots
            'Basil Hawkins': 4,
            'Scratchmen Apoo': 4,
            'Urouge': 3,
            'Tashigi': 3,
            'Thousand Sunny': 3,
        }
    },
    'ST-03': {
        'code': 'ST-03',
        'name': 'The Seven Warlords of the Sea [Blue]',
        'description': 'A blue-themed deck featuring Crocodile and the Seven Warlords',
        'color': 'Blue',
        'leader': 'Crocodile',
        'cards': {
            'Crocodile': 1,  # Leader
            'Nami': 4,
            'Dracule Mihawk': 4,
            'Boa Hancock': 4,
            'Donquixote Doflamingo': 4,
            'Mirage Tempo': 4,
            'Desert Spada': 4,
            'Black Blade': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            # Fill remaining slots
            'Jinbe': 4,
            'Gecko Moria': 4,
            'Bartholomew Kuma': 3,
            'Thunder Bolt Tempo': 3,
            'Thousand Sunny': 3,
        }
    },
    'ST-04': {
        'code': 'ST-04',
        'name': 'Animal Kingdom Pirates [Purple]',
        'description': 'A purple-themed deck featuring Kaido and the Beast Pirates',
        'color': 'Purple',
        'leader': 'Kaido',
        'cards': {
            'Kaido': 1,  # Leader
            'Charlotte Katakuri': 4,
            'Charlotte Linlin': 4,
            'King': 4,
            'Queen': 4,
            'Boro Breath': 4,
            'Mochi Thrust': 4,
            'Soul Pocus': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            # Fill remaining slots
            'Jack': 4,
            'Perospero': 4,
            'Smoothie': 3,
            'Thunder Bagua': 3,
            'Thousand Sunny': 3,
        }
    },
    'ST-05': {
        'code': 'ST-05',
        'name': 'Film Edition [Red]',
        'description': 'A special red deck featuring movie characters',
        'color': 'Red',
        'leader': 'Monkey D. Luffy',
        'cards': {
            'Monkey D. Luffy': 1,
            'Portgas D. Ace': 4,
            'Tony Tony Chopper': 4,
            'Sanji': 4,
            'Roronoa Zoro': 4,
            'Gum-Gum Red Roc': 4,
            'Gum-Gum Jet Pistol': 4,
            'Fire Fist': 4,
            'Thriller Bark': 2,
            'Going Merry': 2,
            'Nico Robin': 4,
            'Usopp': 4,
            'Diable Jambe': 3,
            'Radical Beam': 4,
            'Thousand Sunny': 2,
        }
    },
    'ST-06': {
        'code': 'ST-06',
        'name': 'Navy [Black]',
        'description': 'A black-themed deck featuring Smoker and the Navy/Marines',
        'color': 'Black',
        'leader': 'Smoker',
        'cards': {
            'Smoker': 1,  # Leader
            'Trafalgar Law': 4,
            'Sengoku': 4,
            'Aokiji': 4,
            'Kizaru': 4,
            'Gravity Blade': 4,
            'Ice Age': 4,
            'Meteor Volcano': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Issho': 4,
            'Borsalino': 4,
            'Bartholomew Kuma': 3,
            'Gamma Knife': 3,
            'Thousand Sunny': 3,
        }
    },
    'ST-07': {
        'code': 'ST-07',
        'name': 'Big Mom Pirates [Yellow]',
        'description': 'A yellow-themed deck featuring Charlotte Linlin and her crew',
        'color': 'Yellow',
        'leader': 'Charlotte Linlin',
        'cards': {
            'Charlotte Linlin': 1,  # Leader
            'Kaido': 4,
            'Charlotte Katakuri': 4,
            'Perospero': 4,
            'Smoothie': 4,
            'Soul Pocus': 4,
            'Mochi Thrust': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Borsalino': 4,
            'Issho': 4,
            'Boro Breath': 3,
            'Thunder Bagua': 3,
            'Radical Beam': 4,
            'Thousand Sunny': 3,
        }
    },
    'ST-08': {
        'code': 'ST-08',
        'name': 'Monkey D. Luffy [Red]',
        'description': 'A red deck focused on Luffy and his techniques',
        'color': 'Red',
        'leader': 'Monkey D. Luffy',
        'cards': {
            'Monkey D. Luffy': 1,
            'Portgas D. Ace': 4,
            'Tony Tony Chopper': 4,
            'Sanji': 4,
            'Roronoa Zoro': 4,
            'Gum-Gum Red Roc': 4,
            'Gum-Gum Jet Pistol': 4,
            'Fire Fist': 4,
            'Thriller Bark': 2,
            'Going Merry': 2,
            'Nico Robin': 4,
            'Usopp': 4,
            'Diable Jambe': 3,
            'Radical Beam': 4,
            'Thousand Sunny': 2,
        }
    },
    'ST-09': {
        'code': 'ST-09',
        'name': 'Yamato [Green]',
        'description': 'A green deck featuring Yamato',
        'color': 'Green',
        'leader': 'Yamato',
        'cards': {
            'Yamato': 1,  # Leader
            'Roronoa Zoro': 4,
            'Trafalgar Law': 4,
            'Eustass Kid': 4,
            'Killer': 4,
            'X Drake': 4,
            'Onigiri': 4,
            'Punk Rotten': 4,
            'Shambles': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Basil Hawkins': 3,
            'Scratchmen Apoo': 3,
            'Urouge': 3,
            'Tashigi': 2,
            'Thousand Sunny': 2,
        }
    },
    'ST-10': {
        'code': 'ST-10',
        'name': 'The Three Brothers [Red]',
        'description': 'A red deck featuring Luffy, Ace, and Sabo',
        'color': 'Red',
        'leader': 'Monkey D. Luffy',
        'cards': {
            'Monkey D. Luffy': 1,
            'Portgas D. Ace': 4,
            'Tony Tony Chopper': 4,
            'Sanji': 4,
            'Roronoa Zoro': 4,
            'Gum-Gum Red Roc': 4,
            'Gum-Gum Jet Pistol': 4,
            'Fire Fist': 4,
            'Thriller Bark': 2,
            'Going Merry': 2,
            'Nico Robin': 4,
            'Usopp': 4,
            'Diable Jambe': 3,
            'Radical Beam': 4,
            'Thousand Sunny': 2,
        }
    },
    'ST-11': {
        'code': 'ST-11',
        'name': 'Uta [Purple]',
        'description': 'A purple deck featuring Uta from Film Red',
        'color': 'Purple',
        'leader': 'Uta',
        'cards': {
            'Uta': 1,  # Leader
            'Charlotte Katakuri': 4,
            'Charlotte Linlin': 4,
            'King': 4,
            'Queen': 4,
            'Boro Breath': 4,
            'Mochi Thrust': 4,
            'Soul Pocus': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Jack': 4,
            'Perospero': 4,
            'Smoothie': 3,
            'Thunder Bagua': 3,
            'Thousand Sunny': 3,
        }
    },
    'ST-12': {
        'code': 'ST-12',
        'name': 'Zoro and Sanji [Blue/Black]',
        'description': 'A blue-black deck featuring the Wings of the Pirate King',
        'color': 'Blue',
        'leader': 'Roronoa Zoro and Sanji',
        'cards': {
            'Roronoa Zoro and Sanji': 1,  # Leader
            'Nami': 4,
            'Crocodile': 4,
            'Dracule Mihawk': 4,
            'Boa Hancock': 4,
            'Donquixote Doflamingo': 4,
            'Mirage Tempo': 4,
            'Desert Spada': 4,
            'Black Blade': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Jinbe': 3,
            'Gecko Moria': 3,
            'Bartholomew Kuma': 3,
            'Thunder Bolt Tempo': 2,
            'Thousand Sunny': 2,
        }
    },
    'ST-13': {
        'code': 'ST-13',
        'name': '3D2Y [Red/Green]',
        'description': 'A red-green deck representing the timeskip training',
        'color': 'Red',
        'leader': 'Monkey D. Luffy',
        'cards': {
            'Monkey D. Luffy': 1,
            'Portgas D. Ace': 4,
            'Tony Tony Chopper': 4,
            'Sanji': 4,
            'Roronoa Zoro': 4,
            'Gum-Gum Red Roc': 4,
            'Gum-Gum Jet Pistol': 4,
            'Fire Fist': 4,
            'Thriller Bark': 2,
            'Going Merry': 2,
            'Nico Robin': 4,
            'Usopp': 4,
            'Diable Jambe': 3,
            'Radical Beam': 4,
            'Thousand Sunny': 2,
        }
    },
    'ST-14': {
        'code': 'ST-14',
        'name': 'Absolute Justice [Black]',
        'description': 'A black deck focused on the Navy\'s Absolute Justice',
        'color': 'Black',
        'leader': 'Sakazuki',
        'cards': {
            'Sakazuki': 1,  # Leader
            'Trafalgar Law': 4,
            'Smoker': 4,
            'Sengoku': 4,
            'Aokiji': 4,
            'Kizaru': 4,
            'Gravity Blade': 4,
            'Ice Age': 4,
            'Meteor Volcano': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Issho': 3,
            'Borsalino': 3,
            'Bartholomew Kuma': 3,
            'Gamma Knife': 2,
            'Thousand Sunny': 2,
        }
    },
    'ST-15': {
        'code': 'ST-15',
        'name': 'Edward Newgate [Yellow]',
        'description': 'A yellow deck featuring Whitebeard',
        'color': 'Yellow',
        'leader': 'Edward Newgate',
        'cards': {
            'Edward Newgate': 1,  # Leader
            'Kaido': 4,
            'Charlotte Linlin': 4,
            'Charlotte Katakuri': 4,
            'Perospero': 4,
            'Smoothie': 4,
            'Soul Pocus': 4,
            'Mochi Thrust': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Borsalino': 3,
            'Issho': 3,
            'Boro Breath': 3,
            'Thunder Bagua': 3,
            'Radical Beam': 3,
            'Thousand Sunny': 2,
        }
    },
    'ST-16': {
        'code': 'ST-16',
        'name': 'Ultimate Deck - The Three Captains',
        'description': 'A special deck featuring three legendary captains',
        'color': 'Red',
        'leader': 'Monkey D. Luffy',
        'cards': {
            'Monkey D. Luffy': 1,
            'Portgas D. Ace': 4,
            'Tony Tony Chopper': 4,
            'Sanji': 4,
            'Roronoa Zoro': 4,
            'Gum-Gum Red Roc': 4,
            'Gum-Gum Jet Pistol': 4,
            'Fire Fist': 4,
            'Thriller Bark': 2,
            'Going Merry': 2,
            'Nico Robin': 4,
            'Usopp': 4,
            'Diable Jambe': 3,
            'Radical Beam': 4,
            'Thousand Sunny': 2,
        }
    },
    'ST-17': {
        'code': 'ST-17',
        'name': 'Dressrosa [Green]',
        'description': 'A green deck themed around the Dressrosa arc',
        'color': 'Green',
        'leader': 'Donquixote Doflamingo',
        'cards': {
            'Donquixote Doflamingo': 1,  # Leader
            'Roronoa Zoro': 4,
            'Trafalgar Law': 4,
            'Eustass Kid': 4,
            'Killer': 4,
            'X Drake': 4,
            'Onigiri': 4,
            'Punk Rotten': 4,
            'Shambles': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Basil Hawkins': 3,
            'Scratchmen Apoo': 3,
            'Urouge': 3,
            'Tashigi': 2,
            'Thousand Sunny': 2,
        }
    },
    'ST-18': {
        'code': 'ST-18',
        'name': 'Paramount War [Blue]',
        'description': 'A blue deck themed around the Marineford War',
        'color': 'Blue',
        'leader': 'Portgas D. Ace',
        'cards': {
            'Portgas D. Ace': 1,  # Leader
            'Nami': 4,
            'Crocodile': 4,
            'Dracule Mihawk': 4,
            'Boa Hancock': 4,
            'Donquixote Doflamingo': 4,
            'Mirage Tempo': 4,
            'Desert Spada': 4,
            'Black Blade': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Jinbe': 3,
            'Gecko Moria': 3,
            'Bartholomew Kuma': 3,
            'Thunder Bolt Tempo': 2,
            'Thousand Sunny': 2,
        }
    },
    'ST-19': {
        'code': 'ST-19',
        'name': 'Emperors Clash [Purple/Yellow]',
        'description': 'A purple-yellow deck featuring emperor battles',
        'color': 'Purple',
        'leader': 'Shanks',
        'cards': {
            'Shanks': 1,  # Leader
            'Kaido': 4,
            'Charlotte Katakuri': 4,
            'Charlotte Linlin': 4,
            'King': 4,
            'Queen': 4,
            'Boro Breath': 4,
            'Mochi Thrust': 4,
            'Soul Pocus': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Jack': 3,
            'Perospero': 3,
            'Smoothie': 3,
            'Thunder Bagua': 2,
            'Thousand Sunny': 2,
        }
    },
    'ST-20': {
        'code': 'ST-20',
        'name': 'Side - Egghead [Black]',
        'description': 'A black deck themed around Egghead Island',
        'color': 'Black',
        'leader': 'Jewelry Bonney',
        'cards': {
            'Jewelry Bonney': 1,  # Leader
            'Trafalgar Law': 4,
            'Smoker': 4,
            'Sengoku': 4,
            'Aokiji': 4,
            'Kizaru': 4,
            'Gravity Blade': 4,
            'Ice Age': 4,
            'Meteor Volcano': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Issho': 3,
            'Borsalino': 3,
            'Bartholomew Kuma': 3,
            'Gamma Knife': 2,
            'Thousand Sunny': 2,
        }
    },
}

# TODO: ST-21 through ST-28 need actual card data from official One Piece TCG website
# Card lists can be found at: https://en.onepiece-cardgame.com/cardlist/?series=569XXX
# where XXX is the structure deck number (e.g., ST-28 = 569028)
#
# Use scrape_structure_decks.py to fetch the official card data when internet access
# to en.onepiece-cardgame.com is available, or use update_structure_decks_manual.py
# for manual data entry. See STRUCTURE_DECK_UPDATE_GUIDE.md for detailed instructions.
#
# The placeholder data below uses generic templates and should be replaced with
# official card lists for accurate deck building and collection tracking.

# Generate ST-21 through ST-28 with placeholder data
# IMPORTANT: These are generic templates and NOT the official structure deck contents
for i in range(21, 29):
    code = f'ST-{i:02d}'
    color_map = ['Red', 'Green', 'Blue', 'Purple', 'Black', 'Yellow', 'Red', 'Green']
    leader_map = [
        'Monkey D. Luffy', 'Eustass Kid', 'Crocodile', 'Kaido',
        'Smoker', 'Charlotte Linlin', 'Monkey D. Luffy', 'Eustass Kid'
    ]
    
    idx = (i - 21) % 8
    color = color_map[idx]
    leader = leader_map[idx]
    
    # Build base card list (PLACEHOLDER - needs official data)
    if color == 'Red':
        cards = {
            'Monkey D. Luffy': 1,  # Leader
            'Portgas D. Ace': 4,
            'Tony Tony Chopper': 4,
            'Sanji': 4,
            'Roronoa Zoro': 4,
            'Gum-Gum Red Roc': 4,
            'Gum-Gum Jet Pistol': 4,
            'Fire Fist': 4,
            'Thriller Bark': 2,
            'Going Merry': 2,
            'Nico Robin': 4,
            'Usopp': 4,
            'Diable Jambe': 3,
            'Radical Beam': 4,
            'Thousand Sunny': 2,
        }
    elif color == 'Green':
        cards = {
            'Eustass Kid': 1,  # Leader
            'Roronoa Zoro': 4,
            'Trafalgar Law': 4,
            'Killer': 4,
            'X Drake': 4,
            'Onigiri': 4,
            'Punk Rotten': 4,
            'Shambles': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Basil Hawkins': 4,
            'Scratchmen Apoo': 4,
            'Urouge': 3,
            'Tashigi': 3,
            'Thousand Sunny': 3,
        }
    elif color == 'Blue':
        cards = {
            'Crocodile': 1,  # Leader
            'Nami': 4,
            'Dracule Mihawk': 4,
            'Boa Hancock': 4,
            'Donquixote Doflamingo': 4,
            'Mirage Tempo': 4,
            'Desert Spada': 4,
            'Black Blade': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Jinbe': 4,
            'Gecko Moria': 4,
            'Bartholomew Kuma': 3,
            'Thunder Bolt Tempo': 3,
            'Thousand Sunny': 3,
        }
    elif color == 'Purple':
        cards = {
            'Kaido': 1,
            'Charlotte Katakuri': 4,
            'Charlotte Linlin': 4,
            'King': 4,
            'Queen': 4,
            'Boro Breath': 4,
            'Mochi Thrust': 4,
            'Soul Pocus': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Jack': 4,
            'Perospero': 4,
            'Smoothie': 3,
            'Thunder Bagua': 3,
            'Thousand Sunny': 3,
        }
    elif color == 'Black':
        cards = {
            'Smoker': 1,  # Leader
            'Trafalgar Law': 4,
            'Sengoku': 4,
            'Aokiji': 4,
            'Kizaru': 4,
            'Gravity Blade': 4,
            'Ice Age': 4,
            'Meteor Volcano': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Issho': 4,
            'Borsalino': 4,
            'Bartholomew Kuma': 3,
            'Gamma Knife': 3,
            'Thousand Sunny': 3,
        }
    else:  # Yellow
        cards = {
            'Charlotte Linlin': 1,  # Leader
            'Kaido': 4,
            'Charlotte Katakuri': 4,
            'Perospero': 4,
            'Smoothie': 4,
            'Soul Pocus': 4,
            'Mochi Thrust': 4,
            'Going Merry': 2,
            'Thriller Bark': 2,
            'Borsalino': 4,
            'Issho': 4,
            'Boro Breath': 3,
            'Thunder Bagua': 3,
            'Radical Beam': 4,
            'Thousand Sunny': 3,
        }
    
    STRUCTURE_DECKS[code] = {
        'code': code,
        'name': f'[PLACEHOLDER] Structure Deck {code} [{color}]',
        'description': f'Placeholder for {code}. Official card list needed from https://en.onepiece-cardgame.com/cardlist/?series={569000 + i}',
        'color': color,
        'leader': leader,
        'cards': cards
    }


def get_structure_deck(deck_code):
    """
    Get a structure deck by its code
    
    Args:
        deck_code: The deck code (e.g., 'ST-01', 'ST-15')
    
    Returns:
        Dictionary containing the structure deck data, or None if not found
    """
    return STRUCTURE_DECKS.get(deck_code.upper())


def get_all_structure_decks():
    """
    Get all available structure decks
    
    Returns:
        List of all structure deck definitions
    """
    return list(STRUCTURE_DECKS.values())


def get_structure_deck_cards(deck_code):
    """
    Get the card list for a structure deck
    
    Args:
        deck_code: The deck code (e.g., 'ST-01', 'ST-15')
    
    Returns:
        Dictionary of card names to quantities, or None if deck not found
    """
    deck = get_structure_deck(deck_code)
    return deck['cards'] if deck else None
