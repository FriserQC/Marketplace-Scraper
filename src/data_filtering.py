import re

UNWANTED_WORDS = [
    'offre', 'offer', 'offres', 'offers', 
    'vente', 'ventes', 'vendre', 'vends', 'vendons', 'vendez', 'vendent', 
    'sale', 'sales', 'liquidation', 'liquidations', 'solde', 'soldes',
    'rabais', 'deal', 'promotion', 'promotions', 'discount', 'discounts', 'savings',
    'buy', 'buying', 'acheter', 'achete', 'achète', 'achetes', 'achètes', 
    'sell', 'selling', 
    'louer', 'rent', 'location', 'locations', 
    'price', 'prices', 'prix',  'pricing',
    'cash', 'paiement', 'paiements', 'payment', 'payments', 'pay', 
    'taxes', 'taxe', 'tax', 
    'rate', 'rates',
    'not free', 'pas gratuit', 'pas gratuits', 
    'remboursable', 'remboursables', 'remboursement', 'remboursements',
    'financement', 'financing', 'finance', 
    'credit', 'crédit', 
    'free shipping', 'fast shipping', 'free delivery', 'fast delivery', 'delivery available', 'quality delivery',
    'livraison gratuite', 'livraison rapide', 
    'installation', 'service', 'services',
    'commande', 'commandes', 'order', 'orders',
    'lifetime warranty',
    'negotiable', 'negociable', 'négociable', 
    'recherche', 'recherches', 'recherchons', 'recherchez', 'recherchent',
    'échange', 'echange', 'échanges', 'echanges', 'échanger', 
    'exchange', 'exchanges', 'trade', 'trades',
    'soumission', 'quote', 'estimé', 'estimés'
]

FURNITURE_WORDS = [
    'meuble', 'meubles', 'furniture', 'furnitures', 
    'bureau', 'bureaux', 'desk', 'desks', 
    'tiroir', 'tiroirs', 'drawer', 'drawers', 
    'dresser', 
    'chaise', 'chaises', 'chair', 'chairs', 
    'commode', 'commodes', 
    'ottoman', 'ottomans', 
    'sofa', 'sofas', 'divan', 'divans', 
    'fauteuil', 'fauteuils', 'futon', 'futons', 
    'causeuse', 'causeuses', 
    'canapé', 'canapés', 'canape', 
    'sectionnelle', 'sectionnelles', 'sectional', 
    'couch', 'couchs', 
    'lit', 'lits', 'bed', 'beds', 
    'bibliothèque', 'bibliotheque', 'bibliothèques', 
    'bibliotheque', 'bookcase', 'bookcases', 
    'armoire', 'armoires', 'cabinet', 'cabinets', 
    'classeur', 'classeurs', 
    'buffet', 'buffets', 
    'tablette', 'tablettes', 'étagères', 'étagère', 
    'table', 'tables', 
    'lampe', 'lampes', 'lamp', 'lamps', 
    'luminaire', 'luminaires', 
    'sommier', 'sommeiler', 'matelas', 
    'box spring', 'box springs', 
    'laveuse', 'washer', 'sècheuse', 'dryer', 
    'cuisine', 'cuisines', 'kitchen', 'kitchens', 
    'frigo', 'frigos', 'frigidaire', 'frigidaires', 
    'fridge', 'fridges', 'refrigerator', 'refrigerators', 
    'congélateur', 'congélateurs', 'congelateur', 'congelateurs', 
    'cuisinière', 'cuisiniere', 'cuisinières', 'cuisinieres', 
    'micro-onde', 'microonde', 'micro onde', 'micro-ondes', 
    'microondes', 'micro ondes', 'microwave', 'microwaves', 
    'foyer', 'foyers', 'fireplace', 'fireplaces', 
    'rideau', 'rideaux', 'curtain', 'curtains', 
    'coussin', 'coussins', 'cushion', 'cushions', 
    'oreiller', 'oreillers', 'pillow', 'pillows', 
    'coffre', 'coffres', 'miroir', 'miroirs', 
    'mirror', 'mirrors', 
    'cadre', 'cadres', 'frame', 'frames', 
    'piano', 'pianos', 
    'piscine', 'piscines', 'pool', 'pools', 
    'spa', 'spas'
]

WANTED_CATEGORIES = ['Electronics', 'Musical Instruments', 'Sporting Goods']
UNWANTED_CATEGORIES = ['Vehicles', 'Property Rentals', 'Home Sales']
HOME_CATEGORIES = ['Home Goods', 'Home Improvement Supplies', 'Garden & Outdoor', 'Pet Supplies', 'Office Supplies', 'Family', 'Toys & Games']

def is_unwanted_string(string_to_check):
    # Check if the given string contains unwanted words or a dollar sign
    string_to_check = string_to_check.lower().replace('\n', ' ').strip()

    # Check if contains $ in string
    if re.search(r"\$", string_to_check):
        return True

    # Check for unwanted words
    return any(word_is_in_string(word, string_to_check) for word in UNWANTED_WORDS)

def is_furniture(wordToCheck):
    # Determine if contains furniture-related words
    return any(word_is_in_string(word, wordToCheck) for word in FURNITURE_WORDS)

def word_is_in_string(word, string_to_check):
    # Check if a word is present in the given string
    pattern = re.compile(rf"\b(?:{word})\b", re.IGNORECASE)
    return bool(pattern.search(string_to_check))

def determine_categories(listings):
    # Determine the categories of the listings

    for listing in listings:
        if is_unwanted_string(listing.description) or any(listing.general_category == word for word in UNWANTED_CATEGORIES) or listing.specific_category == "Cars & Trucks" or listing.specific_category == "Commercial Trucks":
            listing.is_unwanted = True
        elif is_furniture(listing.title) or is_furniture(listing.description) or is_furniture(listing.general_category) or is_furniture(listing.specific_category):
            listing.is_furniture = True
        elif any(listing.general_category == word for word in WANTED_CATEGORIES) or "Outdoor" in listing.specific_category:
            listing.is_wanted = True
        elif any(listing.general_category == word for word in HOME_CATEGORIES):
            listing.is_home = True

    return listings
