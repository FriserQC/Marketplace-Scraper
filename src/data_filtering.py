import re

UNWANTED_WORDS = [
    'offre', 'offer', 'offres', 'offers', 'sale', 'sales', 'wholesale',
    'wholesales', 'clearance', 'clearances', 'liquidation', 'liquidations',
    'vente', 'ventes', 'rabais', 'deal', 'vendre', 'vend', 'vends', 'vendons',
    'vendez', 'vendent', 'sell', 'selling', 'louer', 'rent', 'location',
    'locations', 'price', 'prices', 'prix', 'cash', 'paiement', 'paiements',
    'payment', 'payments', 'pay', 'cad', 'usd', 'taxes', 'taxe', 'tax',
    'not free', 'pas gratuit', 'pas gratuits', 'achete', 'achète', 'achetes',
    'achètes', 'acheter', 'buy', 'buying', 'échange', 'echange', 'échanges',
    'echanges', 'échanger', 'echanger', 'trade', 'trades', 'trading', 
    'exchange', 'exchanges', 'échangeable', 'échangeables', 'echangeables', 
    'echangeable', 'remboursable', 'remboursables', 'negotiable', 
    'negotiables', 'négociable', 'negociable', 'négociables', 'negociables',
    'credit', 'crédit', 'soumission', 'quote', 'free shipping', 
    'fast shipping', 'free delivery', 'fast delivery', 'livraison gratuite',
    'livraison rapide', 'financement', 'financing', 'finance', 
    'recherche', 'recherches', 'recherchons', 'recherchez', 'recherchent'
]

FURNITURE_WORDS = [
    'meuble', 'meubles', 'furniture', 'furnitures', 'bureau', 'bureaux',
    'desk', 'desks', 'tiroir', 'tiroirs', 'drawer', 'drawers', 'dresser',
    'chaise', 'chaises', 'chair', 'chairs', 'commode', 'commodes', 
    'ottoman', 'ottomans', 'sofa', 'sofas', 'divan', 'divans', 
    'fauteuil', 'fauteuils', 'futon', 'futons', 'causeuse', 
    'causeuses', 'canapé', 'canapés', 'canape', 'sectionnelle', 
    'sectionnelles', 'sectional', 'couch', 'couchs', 'bed', 'beds', 
    'lit', 'lits', 'bibliothèque', 'bibliotheque', 'bibliothèques', 
    'bibliotheque', 'bookcase', 'bookcases', 'armoire', 'armoires', 
    'cabinet', 'cabinets', 'classeur', 'classeurs', 'filiere', 
    'filieres', 'filière', 'filières', 'buffet', 'buffets', 
    'tablette', 'tablettes', 'étagères', 'étagère', 'table', 'tables', 
    'lampe', 'lampes', 'lamp', 'lamps', 'luminaire', 'luminaires', 
    'sommier', 'sommeiler', 'matelas', 'box spring', 'box springs', 
    'laveuse', 'washer', 'sècheuse', 'dryer', 'cuisine', 'cuisines', 
    'kitchen', 'kitchens', 'frigo', 'frigos', 'frigidaire', 'frigidaires', 
    'fridge', 'fridges', 'refrigerator', 'refrigerators', 'congélateur', 
    'congélateurs', 'congelateur', 'congelateurs', 'congelo', 'congélo',  
    'congelos', 'congélos', 'cuisinière', 'cuisiniere', 'cuisinières', 
    'cuisinieres', 'micro-onde', 'microonde', 'micro onde', 'micro-ondes', 
    'microondes', 'micro ondes', 'microwave', 'microwaves', 'foyer', 
    'foyers', 'fireplace', 'fireplaces', 'rideau', 'rideaux', 
    'curtain', 'curtains', 'coussin', 'coussins', 'cushion', 
    'cushions', 'oreiller', 'oreillers', 'pillow', 'pillows', 
    'coffre', 'coffres', 'miroir', 'miroirs', 'mirror', 'mirrors', 
    'cadre', 'cadres', 'frame', 'frames', 'piano', 'pianos', 
    'piscine', 'piscines', 'pool', 'pools', 'spa', 'spas'
]

def is_unwanted_string(string_to_check):
    # Check if the given string contains unwanted words or a dollar sign
    string_to_check = string_to_check.lower().replace('\n', ' ').strip()

    # Check if contains $ in string
    if re.search(r"\$", string_to_check):
        return True

    # Check for unwanted words
    return any(word_is_in_string(word, string_to_check) for word in UNWANTED_WORDS)

def is_furniture(title, description):
    # Determine if the title or description contains furniture-related words
    return any(word_is_in_string(word, description) or word_is_in_string(word, title) for word in FURNITURE_WORDS)

def word_is_in_string(word, string_to_check):
    # Check if a word is present in the given string
    pattern = re.compile(rf"\b(?:{word})\b", re.IGNORECASE)
    return bool(pattern.search(string_to_check))
