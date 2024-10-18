import re

UNWANTED_WORDS = ['offre', 'offer', 'offres', 'offers',
                  'sale', 'sales', 'wholesale', 'wholesales', 'clearance', 'clearances', 'liquidation', 'liquidations', 'vente', 'ventes', 'rabais', 'deal',
                  'vendre', 'vend', 'vends', 'vendons', 'vendez', 'vendent', 'sell', 'selling', 
                  'louer', 'rent', 'location', 'locations',
                  'price', 'prices', 'prix', 'cash',
                  'not free', 'pas gratuit', 'pas gratuits',
                  'negotiable', 'negotiables', 'négociable', 'negociable', 'négociables', 'negociables',
                  'échange', 'echange', 'échanges', 'echanges', 'échanger', 'echanger', 'trade', 'trades', 'trading', 'exchange', 'exchanges',
                  'achete', 'achète', 'achetes', 'achètes', 'acheter', 'buy', 'buying',
                  'échangeable', 'échangeables', 'echangeables', 'echangeable', 'remboursable', 'remboursables',
                  'credit', 'crédit',
                  'soumission', 'quote',
                  'free shipping', 'fast shipping', 'livraison gratuite', 'livraison rapide',
                  'financement', 'financing',
                  'paiement', 'paiements', 'payment', 'payments', 'pay', 
                  'cad', 'usd', 'taxes', 'taxe', 'tax',
                  'recherche', 'recherches', 'recherchons', 'recherchez', 'recherchent']

WANTED_WORDS = ['free', 'gratuit', 
                'donner', 'à donner', 'donné', 'donne', 'give away', 'giving away']

FURNITURE_WORDS = ['meuble', 'meubles', 'furniture', 'furnitures',
                   'bureau', 'bureaux', 'desk', 'desks', 
                   'tiroir', 'tiroirs', 'drawer', 'drawers', 'dresser', 
                   'chaise', 'chaises', 'chair', 'chairs',
                   'commode', 'commodes', 'ottoman', 
                   'sofa', 'sofas', 'divan', 'divans', 'fauteuil', 'fauteuils', 'causeuse', 'causeuses', 'canapé', 'canapés', 'canape', 'sectionnelle', 'sectionnelles', 'sectional', 'couch', 'couchs',
                   'bed', 'beds', 'lit', 'lits',
                   'table', 'tables', 
                   'lampe', 'lampes', 'lamp', 'lamps', 'luminaire', 'luminaires', 
                   'sommier', 'sommeiler', 'matelas', 'box spring',
                   'laveuse', 'washer', 'sècheuse', 'dryer',
                   'frigo', 'frigidaire', 'fridge', 'refrigerator', 'congélateur',
                   'cuisinière', 'cuisiniere', 
                   'micro-onde', 'microonde', 'micro-ondes', 'microondes', 'microwave', 'microwaves',
                   'bibliothèque', 'bibliotheque', 'bookcase', 
                   'foyer', 'fireplace',
                   'armoire', 'armoires', 'cabinet', 'classeur', 'classeurs', 'filiere', 'filieres', 'filière', 'filières',
                   'tablette', 'tablettes', 'étagères', 'étagère',
                   'rideau', 'rideaux', 'curtain', 'curtains',
                   'coffre', 
                   'miroir', 'mirror', 'cadres', 'frames',
                   'piano',
                   'piscine', 'pool', 'spa',
                   'buffet']

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