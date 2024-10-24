import re

UNWANTED_WORDS = ['offre', 'offer', 'offres', 'offers',
                  'sale', 'sales', 'wholesale', 'wholesales', 'clearance', 'clearances', 'liquidation', 'liquidations', 'vente', 'ventes', 'rabais', 'deal',
                  'vendre', 'vend', 'vends', 'vendons', 'vendez', 'vendent', 'sell', 'selling', 
                  'louer', 'rent', 'location', 'locations',
                  'price', 'prices', 'prix', 'cash',
                  'paiement', 'paiements', 'payment', 'payments', 'pay', 
                  'cad', 'usd', 'taxes', 'taxe', 'tax',
                  'not free', 'pas gratuit', 'pas gratuits',
                  'achete', 'achète', 'achetes', 'achètes', 'acheter', 'buy', 'buying',
                  'échange', 'echange', 'échanges', 'echanges', 'échanger', 'echanger', 'trade', 'trades', 'trading', 'exchange', 'exchanges',
                  'échangeable', 'échangeables', 'echangeables', 'echangeable', 'remboursable', 'remboursables',
                  'negotiable', 'negotiables', 'négociable', 'negociable', 'négociables', 'negociables',
                  'credit', 'crédit',
                  'soumission', 'quote',
                  'free shipping', 'fast shipping', 'free delivery', 'fast delivery', 'livraison gratuite', 'livraison rapide',
                  'financement', 'financing', 'finance', 
                  'recherche', 'recherches', 'recherchons', 'recherchez', 'recherchent']

WANTED_WORDS = ['free', 'gratuit', 
                'donner', 'à donner', 'donné', 'donne', 'give away', 'giving away']

FURNITURE_WORDS = ['meuble', 'meubles', 'furniture', 'furnitures',
                   'bureau', 'bureaux', 'desk', 'desks', 
                   'tiroir', 'tiroirs', 'drawer', 'drawers', 'dresser', 
                   'chaise', 'chaises', 'chair', 'chairs',
                   'commode', 'commodes', 'ottoman', 'ottomans',
                   'sofa', 'sofas', 'divan', 'divans', 'fauteuil', 'fauteuils', 'futon', 'futons', 'causeuse', 'causeuses', 'canapé', 'canapés', 'canape', 'sectionnelle', 'sectionnelles', 'sectional', 'couch', 'couchs',
                   'bed', 'beds', 'lit', 'lits',
                   'bibliothèque', 'bibliotheque', 'bibliothèques', 'bibliotheque', 'bookcase', 'bookcases', 
                   'armoire', 'armoires', 'cabinet', 'cabinets', 'classeur', 'classeurs', 'filiere', 'filieres', 'filière', 'filières', 'buffet', 'buffets',
                   'tablette', 'tablettes', 'étagères', 'étagère',
                   'table', 'tables', 
                   'lampe', 'lampes', 'lamp', 'lamps', 'luminaire', 'luminaires', 
                   'sommier', 'sommeiler', 'matelas', 'box spring', 'box springs',
                   'laveuse', 'washer', 'sècheuse', 'dryer',
                   'cuisine', 'cuisines', 'kitchen', 'kitchens',
                   'frigo', 'frigos', 'frigidaire', 'frigidaires', 'fridge', 'fridges', 'refrigerator', 'refrigerators', 'congélateur', 'congélateurs', 'congelateur', 'congelateurs', 'congelo', 'congélo',  'congelos', 'congélos',
                   'cuisinière', 'cuisiniere', 'cuisinières', 'cuisinieres', 
                   'micro-onde', 'microonde', 'micro onde', 'micro-ondes', 'microondes', 'micro ondes', 'microwave', 'microwaves',
                   'foyer', 'foyers', 'fireplace', 'fireplaces',
                   'rideau', 'rideaux', 'curtain', 'curtains',
                   'coussin', 'coussins', 'cushion', 'cushions', 'oreiller', 'oreillers', 'pillow', 'pillows',
                   'coffre', 'coffres',
                   'miroir', 'miroirs', 'mirror', 'mirrors', 'cadre', 'cadres', 'frame', 'frames',
                   'piano', 'pianos',
                   'piscine', 'piscines', 'pool', 'pools', 'spa', 'spas']

def is_unwanted_string(stringToCheck):

    stringToCheck = stringToCheck.lower().replace('\n', ' ').strip()

    # Check if contains $ in string
    checkDollarSign = re.compile(r"\$").search(stringToCheck)
    if checkDollarSign != None:
        return True

    # Check if contains unwanted word only if didn't find dollar sign $
    for word in UNWANTED_WORDS:
        remove = word_is_in_string(word, stringToCheck)
        if remove == True:
            return True

    # Check if contains wanted word             Too many false positives...
    # if remove == True:
    #     for word in WANTED_WORDS:
    #         remove = not word_is_in_string(word, stringToCheck)
    #         if remove == False:
    #             break

    return False

def is_furniture(title, description):

    for word in FURNITURE_WORDS:
            if word_is_in_string(word, description) or word_is_in_string(word, title):
                return True

    return False

def word_is_in_string(word, stringToCheck):

    checks = r"\b(?:"+word+r")\b"
    pattern = re.compile(checks, re.IGNORECASE)
    matched = pattern.search(stringToCheck)
    if matched != None:
        return True
    
    return False