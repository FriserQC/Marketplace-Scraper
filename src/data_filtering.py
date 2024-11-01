import re
from typing import List

UNWANTED_WORDS = [
    # Offers and Sales
    'offre', 'offer', 'offres', 'offers', 'vente', 'ventes', 'vendre', 'vends', 'vendons', 'vendez', 'vendent',
    'sale', 'sales', 'liquidation', 'liquidations', 'solde', 'soldes', 'clearance', 'clearances', 'clearout', 'clearouts', 'clearing', 'clearings',
    'rabais', 'deal', 'promotion', 'promotions', 'promo', 'promos', 'discount', 'discounts', 'savings', 'save', 'saves', 'saving', 'économie', 'économies', 'économiser', 'économisez', 'économisant', 'économisants',

    # Buying and Selling
    'buy', 'buying', 'achete', 'achète', 'achetes', 'achètes', 'achetons', 'achetez', 'achètent', 'achetent',
    'sell', 'selling', 'sells', 'vend',

    # Renting
    'louer', 'rent', 'location', 'locations', 'rental', 'rentals', 'renting', 'rentings',

    # Pricing and Costs
    'price', 'prices', 'prix', 'pricing', 'tarif', 'tarifs', 'cost', 'costs', 'coût', 'coûts',

    # Payments
    'cash', 'paiement', 'paiements', 'payment', 'payments', 'pay', 'pays', 'paying', 'payez', 'payable', 'payables',

    # Taxes
    'taxes', 'taxe', 'tax', 'taxation', 'taxations',

    # Rates
    'rate', 'rates', 'taux',

    # Free and Refunds
    'not free', 'pas gratuit', 'pas gratuits', 'not for free', 'not giveaway', 'not giveaways',
    'remboursable', 'remboursables', 'remboursement', 'remboursements', 'refund', 'refunds',

    # Financing and Credit
    'financement', 'financing', 'finance', 'finances', 'financé', 'financés', 'financée', 'financées',
    'credit', 'crédit', 'crédits', 'credits',

    # Shipping and Delivery
    'free shipping', 'fast shipping', 'free delivery', 'fast delivery', 'delivery available', 'quality delivery',
    'we deliver', 'we ship', 'livraison disponible', 'livraison de qualité',
    'nous livrons', 'nous expédions', 'livraison gratuite', 'livraison rapide',

    # Services and Installation
    'installation', 'installations', 'service', 'services', 'technicien', 'techniciens', 'technicians', 'technician', 'installateur', 'installateurs', 'installers',

    # Orders
    'commande', 'commandes', 'order', 'orders', 'ordering', 'commandez',

    # Warranty
    'lifetime warranty', 'garantie à vie', 'garantie de satisfaction', 'satisfaction guarantee', 'warrantied',

    # Negotiation
    'negotiable', 'negociable', 'négociable', 'négociables', 'negotiables', 'negotiate', 'negotiates', 'negotiating', 'negociate', 'negociates', 'negociating', 'négociation', 'négociations', 'negotiation', 'negotiations',

    # Search
    'recherche', 'recherches', 'recherchons', 'recherchez', 'recherchent',

    # Exchange and Trade
    'échange', 'echange', 'échanges', 'echanges', 'échanger', 'echanger', 'échangent', 'echangent',
    'exchange', 'exchanges', 'trade', 'trades', 'trading', 'traded',

    # Quotes and Estimates
    'soumission', 'quote', 'estimé', 'estimés', 'estimée', 'estimées', 'estimation', 'estimations',
    'soumettre', 'soumet', 'soumettez', 'soumettant', 'soumettent', 'soumissionner', 'soumissionnez', 'soumissionnant', 'soumissionnent',

    # Miscellaneous
    'most demanding'
]

FURNITURE_WORDS = [
    # General Furniture
    'meuble', 'meubles', 'furniture', 'furnitures',

    # Office Furniture
    'bureau', 'bureaux', 'desk', 'desks',

    # Storage Furniture
    'tiroir', 'tiroirs', 'drawer', 'drawers',
    'dresser', 'dressers',
    'commode', 'commodes',
    'armoire', 'armoires', 'cabinet', 'cabinets', 'wardrobe', 'wardrobes',
    'classeur', 'classeurs', 'file cabinet', 'file cabinets',
    'buffet', 'buffets', 'hutch', 'hutches',
    'tablette', 'tablettes', 'étagères', 'étagère', 'shelf', 'shelves',
    'bibliothèque', 'bibliotheque', 'bibliothèques', 'bibliotheques', 'bookshelf', 'bookshelves',
    'bookcase', 'bookcases', 'book case', 'book cases',

    # Seating Furniture
    'chaise', 'chaises', 'chair', 'chairs', 'armchair', 'armchairs',
    'ottoman', 'ottomans', 'pouf', 'poufs',
    'sofa', 'sofas', 'divan', 'divans',
    'fauteuil', 'fauteuils', 'futon', 'futons', 'recliner', 'recliners',
    'causeuse', 'causeuses', 'loveseat', 'loveseats',
    'canapé', 'canapés', 'canape',
    'sectionnelle', 'sectionnelles', 'sectional', 'sectionals',
    'couch', 'couches',

    # Bedroom Furniture
    'lit', 'lits', 'bed', 'beds', 'mattress', 'mattresses',
    'sommier', 'sommeiler', 'matelas',
    'oreiller', 'oreillers', 'pillow', 'pillows', 'pillowcase', 'pillowcases',

    # Lighting
    'lampe', 'lampes', 'lamp', 'lamps', 'lumière', 'lumieres', 'light', 'lights',
    'luminaire', 'luminaires', 'lighting',

    # Kitchen and Appliances
    'cuisine', 'cuisines', 'kitchen', 'kitchens', 'kitchenette', 'kitchenettes',
    'laveuse', 'washer', 'sècheuse', 'dryer', 'laveuse-sécheuse', 'washer-dryer',
    'frigo', 'frigos', 'frigidaire', 'frigidaires', 'réfrigérateur', 'réfrigérateurs',
    'fridge', 'fridges', 'refrigerator', 'refrigerators', 'refrigerateur', 'refrigerateurs',
    'congélateur', 'congélateurs', 'congelateur', 'congelateurs', 'freezer', 'freezers',
    'cuisinière', 'cuisiniere', 'cuisinières', 'cuisinieres', 'stove', 'stoves', 'range', 'ranges',
    'micro-onde', 'microonde', 'micro onde', 'micro-ondes',
    'microondes', 'micro ondes', 'microwave', 'microwaves', 'oven', 'ovens',

    # Miscellaneous
    'foyer', 'foyers', 'fireplace', 'fireplaces', 'cheminée', 'cheminées',
    'rideau', 'rideaux', 'curtain', 'curtains', 'drapery', 'draperies',
    'coussin', 'coussins', 'cushion', 'cushions',
    'coffre', 'coffres', 'miroir', 'miroirs', 'mirror', 'mirrors',
    'cadre', 'cadres', 'frame', 'frames',
    'piscine', 'piscines', 'pool', 'pools',
    'spa', 'spas', 'jacuzzi', 'jacuzzis'
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
