import re
from typing import List

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

def word_is_in_string(word: str, string_to_check: str) -> bool:
    pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
    return bool(pattern.search(string_to_check))

def is_unwanted_string(string_to_check: str) -> bool:
    string_to_check = string_to_check.lower().replace('\n', ' ').strip()
    if re.search(r"\$", string_to_check):
        return True
    return any(word_is_in_string(word, string_to_check) for word in UNWANTED_WORDS)

def determine_categories(listings: List) -> List:
    for listing in listings:
        if (
            is_unwanted_string(listing.description) or 
            listing.general_category in UNWANTED_CATEGORIES or 
            listing.specific_category in ["Cars & Trucks", "Commercial Trucks"]
        ):
            listing.is_unwanted = True
        elif listing.general_category in WANTED_CATEGORIES:
            listing.is_wanted = True
        elif (
            any(word_is_in_string(word, listing.title) for word in FURNITURE_WORDS) or 
            any(word_is_in_string(word, listing.description) for word in FURNITURE_WORDS) or 
            any(word_is_in_string(word, listing.general_category) for word in FURNITURE_WORDS) or 
            any(word_is_in_string(word, listing.specific_category) for word in FURNITURE_WORDS) or 
            listing.general_category in HOME_CATEGORIES
        ):
            listing.is_home = True
    return listings
